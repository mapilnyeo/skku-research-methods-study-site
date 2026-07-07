#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
'떠먹이' 2기 관찰 데이터 — 감성 분석 방법론 전체 파이프라인 (Part 0 → 4).

교수님 제안대로 revealed data에서 두 변인을 사후 분리한다.
  Y  = 사용자 텍스트 감성(파일럿 사전 점수, valence)
  X1 = 인간(운영자) 개입   (측정 가능: actor_type / 타임스탬프 / 카운트)
  X2 = AI 개입 및 'AI 인간유사성'(데이터에 코딩값 없음 → 투명한 텍스트 프록시 지수 사용)

실행:  python analysis/full_pipeline.py /path/to/tteomeogi_csv [--figdir DIR]
의존성: pandas numpy scipy statsmodels linearmodels matplotlib

주의:
  - sentiment_score 는 검증된 분류기가 아니라 파일럿 사전 점수(측정 타당도는 별도 확보 대상).
  - X2 'AI 인간유사성'은 원자료에 없다. 아래는 표면 특징 기반 **프록시**이며, 정식 연구에서는
    사람/LLM 코딩(Part 4-3)으로 대체해야 한다. 프록시임을 결과에 명시한다.
"""
import sys, os, re, argparse
import numpy as np, pandas as pd
from scipy import stats
import statsmodels.api as sm
import statsmodels.formula.api as smf

pd.set_option("display.width", 200)
pd.set_option("display.max_columns", 40)


def h(t): print("\n" + "=" * 78 + f"\n{t}\n" + "=" * 78)


# ---------------------------------------------------------------- load
def load(csv_dir):
    d = {}
    for name in ["users", "student_day_panel", "assignments_posts", "assignments_comments",
                 "qna_posts", "qna_comments", "notices", "events_long"]:
        d[name] = pd.read_csv(f"{csv_dir}/{name}.csv")
    return d


# ====================================================================
# PART 1. 감성을 변수로 — 조작적 정의 · ABSA(대상별) · 측정 신뢰도/타당도
# ====================================================================
def part1(d):
    h("PART 1. 감성 분석 — 댓글을 변수로 (조작적 정의 · 대상 기반 · 신뢰도/타당도)")

    # 1-A/B: 이미 valence 점수(sentiment_score, -1~1)가 있으므로 이를 주 DV로 사용.
    # 1-C 측정 신뢰도: (a) 연속점수 ↔ 라벨 일관성, (b) 연속점수 ↔ (pos-neg) 어휘카운트 일관성
    ap = d["assignments_posts"]
    lab_map = {"positive": 1, "neutral": 0, "negative": -1}
    def consistency(df, src):
        df = df.dropna(subset=["sentiment_score"])
        lab = df["sentiment_label"].map(lab_map)
        # 연속점수 부호와 라벨의 일치율
        agree = (np.sign(df["sentiment_score"]).replace(0, 0) == lab).mean()
        # pos/neg 어휘 카운트 기반 극성과 상관 (construct 내적 일관성)
        if {"positive_count", "negative_count"}.issubset(df.columns):
            lexpol = df["positive_count"] - df["negative_count"]
            r = df["sentiment_score"].corr(lexpol)
        else:
            r = np.nan
        print(f"  [{src:18s}] n={len(df):4d}  점수↔라벨 부호 일치율={agree:.2f}  점수↔(pos-neg)어휘 r={r:.2f}")
    print("1-C 측정 내적 일관성(reliability proxy):")
    consistency(ap, "assignment_post")
    consistency(d["qna_posts"], "qna_post")
    consistency(d["assignments_comments"], "assignment_comment")

    # Construct/face validity: 도움요청(QnA)은 과제제출보다 감성이 낮아야 정상
    print("\n1-C 구성타당도 점검(face validity) — 맥락별 감성이 상식과 맞는가:")
    for src, df in [("과제 제출글", ap), ("Q&A(도움요청)", d["qna_posts"])]:
        s = df["sentiment_score"].dropna()
        print(f"  {src:14s} mean={s.mean():+.3f}  (도움요청이 더 낮으면 타당도 근거)")

    # 1-A(4) 대상 기반(ABSA) 대용: actor_type 로 '개입 주체별 감성' 분리
    print("\n1-A(4) 대상 기반 감성 대용 — assignment 댓글을 작성 주체별로 분리:")
    ac = d["assignments_comments"]
    for a in ["ai_tutor", "human_operator", "participant"]:
        s = ac.loc[ac.actor_type == a, "sentiment_score"].dropna()
        print(f"  {a:15s} n={len(s):4d}  mean={s.mean():+.3f}  neg율={100*(ac.loc[ac.actor_type==a,'sentiment_label']=='negative').mean():.0f}%")
    print("  → 사용자 감성(Y)은 participant 텍스트로 측정하고, ai/human 텍스트는 개입(X)으로 쓴다(대상 분리).")


# ====================================================================
# X2 프록시: AI 응답의 '인간유사성' 표면 지표 (원자료에 없음 → 투명 프록시)
# ====================================================================
def ai_humanlikeness_proxy(ac):
    ai = ac[ac.actor_type == "ai_tutor"].copy()
    t = ai["text_clean"].fillna("")
    # 인간유사 신호(+): 이모티콘/축약/감탄, 짧은 길이, 구조화 마크다운 부재
    emo = t.str.contains(r"[:;][)(D]|ㅎㅎ|ㅋㅋ|~|!!|😊|🙂|👍|❤", regex=True).astype(int)
    structured = t.str.contains(r"(?:^|\n)\s*(?:\d+\.|[-*•]|#|```)", regex=True).astype(int)  # AI다움(-)
    short = (ai["text_length"] < ai["text_length"].median()).astype(int)
    # 0~1 프록시: 인간유사 신호 평균
    ai["hl_proxy"] = (emo + short + (1 - structured)) / 3.0
    return ai[["anon_post_id", "hl_proxy", "created_at_kst"]]


# ====================================================================
# PART 2/3 공통: 사용자×일자 패널 구성 (Part 2-A)
# ====================================================================
def build_panel(d):
    p = d["student_day_panel"].copy()
    p = p[p.is_admin == 0].copy()
    p["date"] = pd.to_datetime(p["kst_date"])
    p = p.sort_values(["anon_user_id", "date"])
    g = p.groupby("anon_user_id", group_keys=False)
    # 개입 발생/누적/도즈
    p["humanFB"] = (p.human_feedback_received_count > 0).astype(int)
    p["aiFB"] = (p.ai_feedback_received_count > 0).astype(int)
    p["humanDose"] = p.human_feedback_received_count
    p["aiDose"] = p.ai_feedback_received_count
    # 시차 항 (직전일)
    p["humanFB_lag1"] = g["humanFB"].shift(1)
    p["aiFB_lag1"] = g["aiFB"].shift(1)
    p["sent"] = p.avg_sentiment_score
    p["sent_lag1"] = g["sent"].shift(1)           # 직전 감성(자기상관 통제)
    p["sent_next"] = g["sent"].shift(-1)          # 익일 감성
    p["active_next"] = g["active_any"].shift(-1)
    # 통제변수
    p["dow"] = p["date"].dt.dayofweek
    p["weekend"] = (p.dow >= 5).astype(int)
    p["t"] = (p["date"] - p["date"].min()).dt.days   # 시간추세
    p["logvol"] = np.log1p(p.event_count)
    return p


# ====================================================================
# PART 2. 시차(time lag) 분석
# ====================================================================
def part2(p, d, figdir):
    h("PART 2. 시차 분석 (event-window t-test · 교차상관 · ITS · 분포시차 · Granger)")
    act = p[p.active_any == 1].copy()
    gg = act.groupby("anon_user_id", group_keys=False)
    act["sent_nextact"] = gg["sent"].shift(-1)   # 다음 '활동일' 감성
    act["delta"] = act["sent_nextact"] - act["sent"]
    dd = act.dropna(subset=["delta"])

    # 2-1 개입 전후 t-test (independent: 인간개입 받은 활동일 vs 아닌 활동일)
    print("2-1 개입 전후 감성 델타 (independent t-test):")
    a = dd.loc[dd.humanFB == 1, "delta"]; b = dd.loc[dd.humanFB == 0, "delta"]
    t, pv = stats.ttest_ind(a, b, equal_var=False)
    print(f"  인간개입 후 Δ={a.mean():+.3f}(n={len(a)}) vs 무개입 Δ={b.mean():+.3f}(n={len(b)}) | t={t:.2f}, p={pv:.3f}")
    a2 = dd.loc[dd.aiFB == 1, "delta"]; b2 = dd.loc[dd.aiFB == 0, "delta"]
    t2, pv2 = stats.ttest_ind(a2, b2, equal_var=False)
    print(f"  AI개입 후   Δ={a2.mean():+.3f}(n={len(a2)}) vs 무개입 Δ={b2.mean():+.3f}(n={len(b2)}) | t={t2:.2f}, p={pv2:.3f}")
    print("  ※ 개입은 원래 감성 높은 날에 붙음 → 평균회귀 의심(Part3 FE에서 재검)")

    # 2-2 교차상관: 일자 집계에서 개입_t 와 감성_{t+k}
    daily = (p[p.active_any == 1].groupby("date")
             .agg(sent=("sent", "mean"), human=("humanDose", "sum"), ai=("aiDose", "sum"),
                  n=("sent", "size")).reset_index().sort_values("date"))
    daily = daily[daily.n >= 3].reset_index(drop=True)   # 표본 얇은 날 제외
    print("\n2-2 교차상관 corr(개입_t, 감성_{t+k}) — 일자 집계:")
    for k in range(0, 4):
        s = daily["sent"].shift(-k)
        rh = daily["human"].corr(s); ra = daily["ai"].corr(s)
        print(f"  k={k}일:  human r={rh:+.2f}   ai r={ra:+.2f}")

    # 2-3 ITS / segmented regression — 커뮤니티 일자 감성에 '미션 종료(Day5=5/7)'를 중단점으로
    print("\n2-3 단절적 시계열(ITS) — 공식 미션기간 종료(2026-05-07)를 중단점으로:")
    its = daily.copy()
    brk = pd.Timestamp("2026-05-07")
    its["time"] = (its.date - its.date.min()).dt.days
    its["post"] = (its.date > brk).astype(int)
    its["time_after"] = np.where(its.post == 1, (its.date - brk).dt.days, 0)
    m = smf.ols("sent ~ time + post + time_after", data=its).fit()
    print(f"  N(일)={len(its)}  β_level(post)={m.params['post']:+.3f} (p={m.pvalues['post']:.3f}),"
          f"  β_slopeΔ(time_after)={m.params['time_after']:+.3f} (p={m.pvalues['time_after']:.3f})")
    print(f"  해석: 미션 종료 직후 수준변화={m.params['post']:+.3f}, 추세변화={m.params['time_after']:+.3f} (T가 작아 검정력 낮음)")

    # 2-4 분포시차 회귀 (패널): 익일 감성 ~ 개입_t + 개입_{t-1} + 통제 + 사용자FE
    print("\n2-4 분포시차 회귀 — 익일 감성 ~ 당일·전일 개입 (사용자 FE, 클러스터 SE):")
    reg = act.dropna(subset=["sent_nextact", "humanFB_lag1", "aiFB_lag1", "sent_lag1"]).copy()
    if len(reg) > 30:
        m2 = smf.ols("sent_nextact ~ humanFB + humanFB_lag1 + aiFB + aiFB_lag1 + sent + sent_lag1 "
                     "+ logvol + weekend + C(anon_user_id)", data=reg).fit(
            cov_type="cluster", cov_kwds={"groups": reg.anon_user_id})
        for k in ["humanFB", "humanFB_lag1", "aiFB", "aiFB_lag1"]:
            if k in m2.params:
                print(f"  {k:14s} β={m2.params[k]:+.3f}  p={m2.pvalues[k]:.3f}")
        hsum = m2.params.get("humanFB", 0) + m2.params.get("humanFB_lag1", 0)
        print(f"  인간개입 누적효과(당일+전일 β합)={hsum:+.3f}")
    else:
        print("  (표본 부족)")

    # 2-5 Granger: 일자 집계에서 human → sent
    print("\n2-5 Granger 인과성(일자 집계, maxlag=2) — human 개입이 감성을 예측하는가:")
    try:
        from statsmodels.tsa.stattools import grangercausalitytests
        gseries = daily[["sent", "human"]].dropna()
        if len(gseries) >= 8:
            res = grangercausalitytests(gseries, maxlag=2, verbose=False)
            for lag in res:
                p_f = res[lag][0]["ssr_ftest"][1]
                print(f"  lag={lag}: p={p_f:.3f}")
            print("  ※ T가 작아(≈일수) 결과는 참고용")
        else:
            print("  (시계열 길이 부족)")
    except Exception as e:
        print("  Granger 생략:", e)

    _fig_timeseries(daily, d, figdir)
    _fig_eventstudy(p, figdir)
    return daily


# ====================================================================
# PART 3. 변인 분리 — 다중회귀 · FE(PanelOLS) · DiD · PSM
# ====================================================================
def part3(p, d):
    h("PART 3. 변인 분리 — 인간개입 X1 과 AI개입/유사성 X2 의 독립효과")
    act = p[p.active_any == 1].copy()
    gg = act.groupby("anon_user_id", group_keys=False)
    act["sent_nextact"] = gg["sent"].shift(-1)

    # 3-A 다중회귀: X1(human) + X2(ai dose) + 통제 (당일 감성 대상)
    print("3-A 다중회귀 — 당일 감성 ~ 인간개입 + AI개입 + 통제(도즈·시간추세·요일·길이·직전감성):")
    reg = act.dropna(subset=["sent", "sent_lag1"]).copy()
    m = smf.ols("sent ~ humanDose + aiDose + t + weekend + logvol + sent_lag1", data=reg).fit(
        cov_type="cluster", cov_kwds={"groups": reg.anon_user_id})
    for k in ["humanDose", "aiDose", "t", "sent_lag1"]:
        print(f"  {k:12s} β={m.params[k]:+.4f}  p={m.pvalues[k]:.3f}")

    # 3-A+ AI 인간유사성 프록시 결합 (개입받은 관측만)
    print("\n3-A+ AI 인간유사성 프록시(X2) 결합 — AI 개입을 받은 활동일 한정:")
    hl = ai_humanlikeness_proxy(d["assignments_comments"])
    # 사용자×일자에 AI 유사성 평균 붙이기 (해당일 사용자가 받은 AI댓글 기준은 원자료 링크 필요 → 근사)
    # 근사: 그 날 커뮤니티 AI 응답의 평균 유사성 (일자 수준 X2)
    hl2 = hl.copy(); hl2["date"] = pd.to_datetime(hl2["created_at_kst"]).dt.normalize()
    hlday = hl2.groupby("date")["hl_proxy"].mean().reset_index()
    aug = act.merge(hlday, on="date", how="left")
    aug = aug[(aug.aiFB == 1)].dropna(subset=["sent", "hl_proxy"])
    print(f"  대상 n={len(aug)} (AI개입 활동일)  AI유사성 프록시 평균={aug.hl_proxy.mean():.2f}")
    if len(aug) > 25:
        m3 = smf.ols("sent ~ humanDose + hl_proxy + t + logvol", data=aug).fit()
        for k in ["humanDose", "hl_proxy"]:
            print(f"  {k:12s} β={m3.params[k]:+.3f}  p={m3.pvalues[k]:.3f}")
        print("  ⚠️ hl_proxy 는 원자료에 없는 표면 프록시. 정식 연구는 사람/LLM 코딩으로 대체.")

    # 3-B FE: PanelOLS entity(사용자)+time 효과
    print("\n3-B 고정효과 패널(PanelOLS) — 사용자+날짜 고정효과, 익일 감성:")
    try:
        from linearmodels.panel import PanelOLS
        fe = act.dropna(subset=["sent_nextact", "sent"]).copy()
        fe = fe.set_index(["anon_user_id", "date"])
        y = fe["sent_nextact"]
        X = fe[["humanFB", "aiFB", "sent", "logvol"]]
        X = sm.add_constant(X)
        res = PanelOLS(y, X, entity_effects=True, time_effects=True,
                       drop_absorbed=True, check_rank=False).fit(cov_type="clustered", cluster_entity=True)
        for k in ["humanFB", "aiFB", "sent"]:
            if k in res.params.index:
                print(f"  {k:10s} β={res.params[k]:+.3f}  p={res.pvalues[k]:.3f}")
        print(f"  N={int(res.nobs)}  within R²={res.rsquared_within:.3f}")
    except Exception as e:
        print("  PanelOLS 대체(OLS+더미):", e)

    # 3-B DiD 이벤트스터디: '첫 인간개입' 상대일(-2..+2) 감성 궤적
    print("\n3-B DiD/event-study — 첫 인간개입 시점 기준 상대일별 평균 감성:")
    es = _event_study_table(p, "humanFB")
    print(es.to_string(index=False))
    print("  해석: 개입 직전(-1)과 직후(+1) 수준 비교. 처치 전 추세가 평평해야 DiD 가정 성립.")

    # 3-B PSM: 인간개입 받을 성향점수 매칭 후 감성 비교
    print("\n3-B 성향점수매칭(PSM) — 개입 성향 매칭 후 당일 감성 비교:")
    _psm(act)


def _event_study_table(p, treatcol):
    rows = []
    for uid, g in p.groupby("anon_user_id"):
        g = g.sort_values("date")
        tr = g[g[treatcol] == 1]
        if tr.empty:
            continue
        t0 = tr["date"].iloc[0]
        gg = g[g.active_any == 1].copy()
        gg["rel"] = (gg["date"] - t0).dt.days
        rows.append(gg[["rel", "sent"]])
    if not rows:
        return pd.DataFrame()
    r = pd.concat(rows)
    r = r[r.rel.between(-2, 2)]
    out = r.groupby("rel").agg(n=("sent", "size"), meanSent=("sent", "mean")).reset_index()
    out["meanSent"] = out["meanSent"].round(3)
    return out


def _psm(act):
    try:
        from sklearn.linear_model import LogisticRegression
        from sklearn.preprocessing import StandardScaler
        df = act.dropna(subset=["sent", "sent_lag1", "logvol"]).copy()
        if df.humanFB.nunique() < 2 or len(df) < 40:
            print("  (표본/변동 부족)"); return
        Xp = df[["sent_lag1", "logvol", "t", "weekend"]].values
        Xp = StandardScaler().fit_transform(Xp)
        ps = LogisticRegression(max_iter=500).fit(Xp, df.humanFB).predict_proba(Xp)[:, 1]
        df["ps"] = ps
        treat = df[df.humanFB == 1]; ctrl = df[df.humanFB == 0]
        # 1:1 최근접 매칭
        matched_c = []
        used = set()
        cps = ctrl["ps"].values
        for _, row in treat.iterrows():
            diffs = np.abs(cps - row["ps"])
            for idx in np.argsort(diffs):
                if idx not in used:
                    used.add(idx); matched_c.append(ctrl.iloc[idx]); break
        mc = pd.DataFrame(matched_c)
        att = treat["sent"].mean() - mc["sent"].mean()
        t, pv = stats.ttest_ind(treat["sent"], mc["sent"], equal_var=False)
        print(f"  매칭쌍 {len(mc)}개  처치 감성={treat['sent'].mean():.3f}  매칭대조={mc['sent'].mean():.3f}"
              f"  ATT={att:+.3f}  (t={t:.2f}, p={pv:.3f})")
    except Exception as e:
        print("  PSM 생략:", e)


# ---------------------------------------------------------------- figures
def _fig_timeseries(daily, d, figdir):
    import warnings, matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    INK, GRID, HUM, AIC = "#1f2933", "#c7cdd4", "#c0392b", "#2b6cb0"
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        fig, ax = plt.subplots(figsize=(9, 4.2), dpi=130)
        ax.axhline(0, color=GRID, lw=1)
        ax.plot(daily.date, daily.sent, "-o", color=INK, lw=2, ms=4, label="Daily mean sentiment (participants)")
        ax.set_ylabel("Mean sentiment (valence)")
        ax.set_ylim(-0.2, 1.0)
        nt = d["notices"].copy()
        nt["date"] = pd.to_datetime(nt["kst_date"])
        first = True
        for dt in sorted(pd.Series(nt["date"].dropna().unique())):
            ax.axvline(pd.Timestamp(dt), color=HUM, alpha=0.22, lw=1,
                       label="Notice (operator)" if first else None); first = False
        ax.axvline(pd.Timestamp("2026-05-07"), color=AIC, ls="--", lw=1.5, label="Mission end (ITS breakpoint)")
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)
        ax.legend(frameon=False, fontsize=8, loc="lower right")
        ax.set_title("Participant sentiment time series with intervention / notice events", fontsize=11)
        fig.autofmt_xdate()
        fig.tight_layout()
        fp = os.path.join(figdir, "fig1_sentiment_timeseries.png")
        fig.savefig(fp); plt.close(fig)
    print(f"\n[figure] {fp}")


def _fig_eventstudy(p, figdir):
    import warnings, matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    es_h = _event_study_table(p, "humanFB")
    es_a = _event_study_table(p, "aiFB")
    if es_h.empty:
        return
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        fig, ax = plt.subplots(figsize=(7.2, 4.2), dpi=130)
        ax.axvline(0, color="#c7cdd4", lw=1)
        ax.plot(es_h.rel, es_h.meanSent, "-o", color="#c0392b", label="Around first HUMAN intervention")
        if not es_a.empty:
            ax.plot(es_a.rel, es_a.meanSent, "-s", color="#2b6cb0", label="Around first AI intervention")
        ax.set_xlabel("Days relative to intervention (0 = intervention day)")
        ax.set_ylabel("Mean sentiment")
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)
        ax.legend(frameon=False, fontsize=9)
        ax.set_title("Event study: sentiment trajectory around interventions", fontsize=11)
        fig.tight_layout()
        fp = os.path.join(figdir, "fig2_event_study.png")
        fig.savefig(fp); plt.close(fig)
    print(f"[figure] {fp}")


# ---------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("csv_dir")
    ap.add_argument("--figdir", default=".")
    a = ap.parse_args()
    os.makedirs(a.figdir, exist_ok=True)
    d = load(a.csv_dir)
    part1(d)
    p = build_panel(d)
    part2(p, d, a.figdir)
    part3(p, d)
    h("완료 — 자세한 해석은 downloads/tteomeogi_2gi_analysis_results.md 참조")


if __name__ == "__main__":
    main()
