#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
'떠먹이' 2기 — 감성 측정을 '제대로 된 한국어 분석기'로 교체 후 재분석.

기존: export에 들어있던 pilot 사전 점수(간이).
교체: KNU 한국어 감성사전(군산대, 14,854엔트리, polarity -2..+2) + KoNLPy Okt 형태소분석 + 부정어 처리.
      → 검증된/공개된 독립 측정치. 두 측정이 같은 결론을 주면 '측정에 강건(robust)'하다는 근거.

주의: 오프라인 프록시가 HuggingFace를 막아 KcELECTRA 다운로드는 불가.
      KNU 사전은 실제 논문에서 널리 쓰이는 정식 리소스로, pilot 대비 명확한 상향.

실행:
  # 1) 사전 내려받기(최초 1회)
  curl -sSL https://raw.githubusercontent.com/park1200656/KnuSentiLex/master/data/SentiWord_info.json -o SentiWord_info.json
  # 2) 실행
  python analysis/knu_reanalysis.py /path/to/tteomeogi_csv SentiWord_info.json
의존성: pandas numpy scipy statsmodels linearmodels konlpy (+ Java)
"""
import sys, json, numpy as np, pandas as pd
from scipy import stats
import statsmodels.api as sm
import statsmodels.formula.api as smf

pd.set_option("display.width", 200)


def h(t): print("\n" + "=" * 78 + f"\n{t}\n" + "=" * 78)


# ---------------------------------------------------------------- KNU scorer
class KnuScorer:
    NEG = {"안", "못", "않다", "없다", "말다", "아니다", "아니"}

    def __init__(self, json_path):
        knu = json.load(open(json_path, encoding="utf-8"))
        self.lex = {}
        for e in knu:
            for key in {e["word"], e.get("word_root", "")}:
                k = key.strip()
                if len(k) >= 2:                       # 1글자 엔트리는 잡음 → 제외
                    self.lex[k] = int(e["polarity"])
        from konlpy.tag import Okt
        self.okt = Okt()

    def score(self, text):
        """반환: (정규화 감성 -1..+1, 감성어 개수)."""
        if not isinstance(text, str) or not text.strip():
            return np.nan, 0
        words = [w for w, _ in self.okt.pos(text, norm=True, stem=True)]
        pol, cnt = 0, 0
        for i, w in enumerate(words):
            if w in self.lex:
                p = self.lex[w]
                if any(words[j] in self.NEG for j in range(max(0, i - 2), i)):
                    p = -p                            # 부정어 창(window) 내 → 부호 반전
                pol += p; cnt += 1
        if cnt == 0:
            return 0.0, 0
        return (pol / cnt) / 2.0, cnt                 # -2..2 평균 → -1..1


# ---------------------------------------------------------------- panel w/ KNU
def rescore_and_build(csv_dir, scorer):
    e = pd.read_csv(f"{csv_dir}/events_long.csv")
    pt = e[(e.actor_type == "participant") & (e.text_clean.notna())].copy()
    sc = pt["text_clean"].apply(lambda t: pd.Series(scorer.score(t), index=["knu", "nmatch"]))
    pt = pd.concat([pt, sc], axis=1)

    # --- 측정 신뢰도/타당도 (Part 1-C) : 새 측정 vs 기존 pilot ---
    h("측정 교체 검증 — KNU(정식 사전) vs pilot(간이)")
    cov = (pt.nmatch > 0).mean()
    r = pt["knu"].corr(pt["sentiment_score"])
    agree = (np.sign(pt["knu"]) == np.sign(pt["sentiment_score"])).mean()
    print(f"참가자 텍스트 {len(pt)}건 | 감성어 커버리지 {cov:.0%} (median {int(pt.nmatch.median())}개)")
    print(f"수렴타당도(convergent validity): Pearson r={r:.2f}, 부호 일치율 {agree:.0%}")
    print("pilot 라벨별 KNU 평균 (단조증가면 타당):")
    print(pt.groupby("sentiment_label")["knu"].mean().round(3).to_string())

    # --- user×date 패널에 KNU 감성 주입 ---
    pt["date"] = pd.to_datetime(pt["kst_date"])
    day = pt.groupby(["anon_user_id", "date"])["knu"].mean().reset_index().rename(columns={"knu": "sent"})

    p = pd.read_csv(f"{csv_dir}/student_day_panel.csv")
    p = p[p.is_admin == 0].copy()
    p["date"] = pd.to_datetime(p["kst_date"])
    p = p.merge(day, on=["anon_user_id", "date"], how="left")
    p = p.sort_values(["anon_user_id", "date"])
    g = p.groupby("anon_user_id", group_keys=False)
    p["humanFB"] = (p.human_feedback_received_count > 0).astype(int)
    p["aiFB"] = (p.ai_feedback_received_count > 0).astype(int)
    p["humanDose"] = p.human_feedback_received_count
    p["aiDose"] = p.ai_feedback_received_count
    p["sent_lag1"] = g["sent"].shift(1)
    p["sent_next"] = g["sent"].shift(-1)
    p["active_next"] = g["active_any"].shift(-1)
    p["weekend"] = (p["date"].dt.dayofweek >= 5).astype(int)
    p["t"] = (p["date"] - p["date"].min()).dt.days
    p["logvol"] = np.log1p(p.event_count)
    return p


# ---------------------------------------------------------------- re-run models
def rerun(p):
    act = p[p.active_any == 1].copy()
    gg = act.groupby("anon_user_id", group_keys=False)
    act["sent_nextact"] = gg["sent"].shift(-1)
    act["delta"] = act["sent_nextact"] - act["sent"]
    dd = act.dropna(subset=["delta"])
    out = {}

    h("재분석 (Y = KNU 감성)")
    # (1) 순진한 전후 t-test
    a = dd.loc[dd.humanFB == 1, "delta"]; b = dd.loc[dd.humanFB == 0, "delta"]
    t, pv = stats.ttest_ind(a, b, equal_var=False)
    out["naive_ttest"] = (a.mean() - b.mean(), pv)
    print(f"(1) 순진한 전후: 인간개입 Δ={a.mean():+.3f}(n={len(a)}) vs 무개입 Δ={b.mean():+.3f}(n={len(b)})  "
          f"차이={a.mean()-b.mean():+.3f}, t={t:.2f}, p={pv:.3f}")

    # (2) 다중회귀 (도즈 + 통제)
    reg = act.dropna(subset=["sent", "sent_lag1"]).copy()
    m = smf.ols("sent ~ humanDose + aiDose + t + weekend + logvol + sent_lag1", data=reg).fit(
        cov_type="cluster", cov_kwds={"groups": reg.anon_user_id})
    out["mreg_human"] = (m.params["humanDose"], m.pvalues["humanDose"])
    print(f"(2) 다중회귀: 인간개입 β={m.params['humanDose']:+.4f} (p={m.pvalues['humanDose']:.3f}), "
          f"AI β={m.params['aiDose']:+.4f} (p={m.pvalues['aiDose']:.3f}), 시간추세 β={m.params['t']:+.4f} (p={m.pvalues['t']:.3f})")

    # (3) 고정효과 PanelOLS
    try:
        from linearmodels.panel import PanelOLS
        fe = act.dropna(subset=["sent_nextact", "sent"]).set_index(["anon_user_id", "date"])
        y = fe["sent_nextact"]; X = sm.add_constant(fe[["humanFB", "aiFB", "sent", "logvol"]])
        res = PanelOLS(y, X, entity_effects=True, time_effects=True,
                       drop_absorbed=True, check_rank=False).fit(cov_type="clustered", cluster_entity=True)
        out["fe_human"] = (res.params.get("humanFB", np.nan), res.pvalues.get("humanFB", np.nan))
        print(f"(3) 고정효과 FE: 인간개입 β={res.params.get('humanFB',float('nan')):+.3f} "
              f"(p={res.pvalues.get('humanFB',float('nan')):.3f}), 직전감성 β={res.params.get('sent',float('nan')):+.3f} "
              f"(p={res.pvalues.get('sent',float('nan')):.3f})  [평균회귀]")
    except Exception as ex:
        print("(3) FE 생략:", ex)

    # (4) PSM
    try:
        from sklearn.linear_model import LogisticRegression
        from sklearn.preprocessing import StandardScaler
        df = act.dropna(subset=["sent", "sent_lag1", "logvol"]).copy()
        Xp = StandardScaler().fit_transform(df[["sent_lag1", "logvol", "t", "weekend"]].values)
        df["ps"] = LogisticRegression(max_iter=500).fit(Xp, df.humanFB).predict_proba(Xp)[:, 1]
        treat = df[df.humanFB == 1]; ctrl = df[df.humanFB == 0]; used = set(); mc = []
        cps = ctrl["ps"].values
        for _, row in treat.iterrows():
            for idx in np.argsort(np.abs(cps - row["ps"])):
                if idx not in used:
                    used.add(idx); mc.append(ctrl.iloc[idx]); break
        mc = pd.DataFrame(mc); att = treat["sent"].mean() - mc["sent"].mean()
        t2, pv2 = stats.ttest_ind(treat["sent"], mc["sent"], equal_var=False)
        out["psm_att"] = (att, pv2)
        print(f"(4) 성향점수매칭 PSM: 매칭 {len(mc)}쌍  ATT={att:+.3f} (t={t2:.2f}, p={pv2:.3f})")
    except Exception as ex:
        print("(4) PSM 생략:", ex)

    return out


def main():
    csv_dir, knu_json = sys.argv[1], sys.argv[2]
    scorer = KnuScorer(knu_json)
    p = rescore_and_build(csv_dir, scorer)
    out = rerun(p)
    h("결론")
    print("교체 전(pilot) → 교체 후(KNU) 인간개입 효과 비교:")
    print(f"  순진한 비교:  pilot t검정 유의(−0.184, p<.001)   →  KNU 차이={out['naive_ttest'][0]:+.3f} (p={out['naive_ttest'][1]:.3f})")
    print(f"  다중회귀:     pilot β≈0(p=.99)                 →  KNU β={out['mreg_human'][0]:+.4f} (p={out['mreg_human'][1]:.3f})")
    if "fe_human" in out:
        print(f"  고정효과:     pilot β=−0.06(p=.35)             →  KNU β={out['fe_human'][0]:+.3f} (p={out['fe_human'][1]:.3f})")
    if "psm_att" in out:
        print(f"  PSM ATT:      pilot −0.001(p=.99)             →  KNU {out['psm_att'][0]:+.3f} (p={out['psm_att'][1]:.3f})")


if __name__ == "__main__":
    main()
