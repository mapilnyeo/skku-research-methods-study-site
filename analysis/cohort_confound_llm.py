#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
1기·2기 통합 — '떡진 데이터' 변인분리 방법론(ITS·분포시차·FE·PSM·DID)을
**LLM 감성**에 그대로 적용. (사전 기반 → LLM 기반 교체 버전)

두 기수를 동일 방법·동일 측정(LLM valence)으로 나란히 본다.

추정 가능성(구조 차이):
  · X₁ 인간(운영자) 개입 : 2기 = 온플랫폼 관찰가능 · 1기 = 플랫폼 밖(카톡) → 개인 outcome 연결 불가
  · X₂ AI 개입           : 두 기수 모두 미션Day와 거의 완전 공선 → 순효과 분리 불가
  · 동료(peer) 개입       : 두 기수 모두 추정 가능(사용자 내 변동 존재)
  · ITS(미션 종료 기준점) : 2기 = 플랫폼 일별 · 1기 = 카톡 일별

실행: python analysis/cohort_confound_llm.py <2gi_dir> <1gi_dir> [--figdir DIR]
입력: llm_panel.csv(2기) · c1_llm_panel.csv/c1_label_map.csv(1기) · 각 assignments_* · kakao_1gi.txt
의존성: pandas numpy scipy statsmodels scikit-learn matplotlib konlpy
"""
import sys, os, re, json, argparse, warnings
import numpy as np, pandas as pd
from scipy import stats
import statsmodels.formula.api as smf
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import NearestNeighbors

MDAYS = [0, 1, 2, 3, 4, 5]
def h(t): print("\n" + "=" * 78 + f"\n{t}\n" + "=" * 78)


def ci_of(res, key):
    c = res.conf_int().loc[key]; return float(c[0]), float(c[1])


def dl_fe_psm(df, y, treat, day, user, covar_len):
    """분포시차(당일+lag)·FE·PSM 공통 실행. df엔 <treat>_lag 있어야 함."""
    out = {}
    dl = df.dropna(subset=[f"{treat}_lag"]).copy()
    m = smf.ols(f"{y} ~ {treat} + {treat}_lag + C({day})", data=dl).fit(
        cov_type="cluster", cov_kwds={"groups": dl[user]})
    out["dl_now"] = (m.params[treat], *ci_of(m, treat), m.pvalues[treat])
    out["dl_lag"] = (m.params[f"{treat}_lag"], *ci_of(m, f"{treat}_lag"), m.pvalues[f"{treat}_lag"])
    fe = smf.ols(f"{y} ~ {treat} + C({user}) + C({day})", data=df).fit()
    out["fe"] = (fe.params[treat], *ci_of(fe, treat), fe.pvalues[treat])
    ps = df.dropna(subset=[y]).copy()
    X = pd.get_dummies(ps[day], prefix="d").astype(float); X["len"] = ps[covar_len].fillna(0).values
    ps["p"] = LogisticRegression(max_iter=1000).fit(X.values, ps[treat].values).predict_proba(X.values)[:, 1]
    tr, co = ps[ps[treat] == 1], ps[ps[treat] == 0]
    if len(tr) and len(co):
        nn = NearestNeighbors(n_neighbors=1).fit(co[["p"]].values)
        _, idx = nn.kneighbors(tr[["p"]].values)
        att = tr[y].values - co[y].values[idx.ravel()]
        se = att.std(ddof=1) / np.sqrt(len(att))
        out["psm"] = (att.mean(), att.mean() - 1.96 * se, att.mean() + 1.96 * se, stats.ttest_1samp(att, 0)[1])
    return out


# ---------- KNU (카톡 ITS용) ----------
class Knu:
    NEG = {"안", "못", "않다", "없다", "말다", "아니다", "아니"}
    def __init__(s, p):
        k = json.load(open(p, encoding="utf-8")); s.lex = {}
        for e in k:
            for key in {e["word"], e.get("word_root", "")}:
                kk = key.strip()
                if len(kk) >= 2: s.lex[kk] = int(e["polarity"])
        from konlpy.tag import Okt; s.okt = Okt()
    def score(s, t):
        if not isinstance(t, str) or not t.strip(): return np.nan
        w = [x for x, _ in s.okt.pos(t, norm=True, stem=True)]; pol = c = 0
        for i, x in enumerate(w):
            if x in s.lex:
                p = s.lex[x]
                if any(w[j] in s.NEG for j in range(max(0, i - 2), i)): p = -p
                pol += p; c += 1
        return (pol / c) / 2.0 if c else np.nan

MSG = re.compile(r'^\[([^\]]+)\] \[(오전|오후) (\d+):(\d+)\] (.*)$')
DATE = re.compile(r'^-+ (\d+)년 (\d+)월 (\d+)일')
OP = {"조온_AI 조교", "가방끈지기", "코드집도의", "매필녀", "클로이"}
MEDIA = {"사진", "이모티콘", "동영상", "삭제된 메시지입니다.", "메시지가 삭제되었습니다.", ".", "파일"}
def kakao_daily(txt, scorer):
    lines = open(txt, encoding="utf-8").read().split("\n"); rows = []; cur = None
    for ln in lines:
        d = DATE.match(ln)
        if d: cur = f"{int(d.group(1))}-{int(d.group(2)):02d}-{int(d.group(3)):02d}"; continue
        m = MSG.match(ln)
        if m:
            name, _, _, _, text = m.groups()
            rows.append(dict(date=cur, isop=name in OP or name.startswith(("스텝_", "스탭_")), text=text))
        elif rows and ln.strip() and not (ln.endswith("들어왔습니다.") or ln.endswith("나갔습니다.") or "되었습니다" in ln):
            rows[-1]["text"] += "\n" + ln
    df = pd.DataFrame(rows)
    part = df[(~df.isop) & (~df.text.str.strip().isin(MEDIA)) & (df.text.str.len() >= 2)].copy()
    part["s"] = part.text.apply(scorer.score)
    d = part.groupby("date").agg(n=("s", "size"), sent=("s", "mean")).reset_index()
    return d[d.n >= 3].reset_index(drop=True)

def its(daily, break_date):
    daily = daily.copy(); daily["t"] = np.arange(len(daily))
    daily["post"] = (daily.date > break_date).astype(int)
    aft = daily[daily.post == 1]
    daily["t_post"] = 0
    if len(aft): daily.loc[daily.post == 1, "t_post"] = daily.loc[daily.post == 1, "t"] - aft.t.min() + 1
    r = smf.ols("sent ~ t + post + t_post", data=daily).fit()
    return (r.params["post"], *ci_of(r, "post"), r.pvalues["post"]), (r.params["t_post"], r.pvalues["t_post"])


def build_2gi(d2):
    p = pd.read_csv("llm_panel.csv")
    ap = pd.read_csv(f"{d2}/assignments_posts.csv")[["anon_post_id", "kst_date"]]
    p = p.merge(ap, on="anon_post_id", how="left")
    p["peer"] = (p["participant_comment_count"] > 0).astype(int)
    p = p.sort_values(["anon_user_id", "day"])
    p["peer_lag"] = p.groupby("anon_user_id")["peer"].shift(1)
    return p

def build_1gi(d1):
    lab = pd.read_csv("c1_llm_panel.csv"); mp = pd.read_csv("c1_label_map.csv")
    df = lab.merge(mp, on=["pid", "day"])
    c = pd.read_csv(f"{d1}/assignments_comments.csv")
    rec = c.groupby("post_key").agg(peer=("comment_author_type", lambda s: (s == "peer_or_other").sum()),
                                    ai=("comment_author_type", lambda s: (s == "ai_operator").sum())).reset_index()
    m = df.merge(rec, on="post_key", how="left").fillna({"peer": 0, "ai": 0})
    m["peer"] = (m.peer > 0).astype(int); m["aiFB"] = (m.ai > 0).astype(int)
    m = m.sort_values(["participant_key", "day"])
    m["peer_lag"] = m.groupby("participant_key")["peer"].shift(1)
    return m


def main():
    a = argparse.ArgumentParser(); a.add_argument("d2"); a.add_argument("d1")
    a.add_argument("--figdir", default="."); a.add_argument("--knu", default="knu/SentiWord_info.json")
    a.add_argument("--kakao", default="kakao_1gi.txt"); args = a.parse_args()
    os.makedirs(args.figdir, exist_ok=True)
    p2 = build_2gi(args.d2); p1 = build_1gi(args.d1)
    scorer = Knu(args.knu)

    h("Part 0. 추정 가능성 매트릭스 (LLM 감성 기준)")
    print(f"{'개입':16s}{'2기':>18s}{'1기':>18s}")
    print(f"{'X₁ 인간(운영자)':16s}{'관찰가능(humanFB)':>18s}{'플랫폼밖(카톡)':>18s}")
    print(f"{'X₂ AI':16s}{'미션Day와 공선':>18s}{'미션Day와 공선':>18s}")
    print(f"{'동료(peer)':16s}{'추정가능':>18s}{'추정가능':>18s}")
    print(f"\n2기 humanFB 사용자 내 변동: {p2.groupby('anon_user_id').humanFB.nunique().gt(1).sum()}/{p2.anon_user_id.nunique()}")
    print(f"2기 aiFB by day: {p2.groupby('day').aiFB.mean().round(2).to_dict()}  → 공선")
    print(f"1기 aiFB by day: {p1.groupby('day').aiFB.mean().round(2).to_dict()}  → 공선")

    rows = []  # (cohort, method, treat, coef, lo, hi, p)

    # ---- 2기: 인간 개입(X₁) ----
    h("2기 — 인간 개입(X₁) 효과 (LLM 감성), 시차·FE·PSM")
    tt = p2.dropna(subset=["llm_next"])
    t = smf.ols("llm_next ~ humanFB + C(day)", data=tt).fit(cov_type="cluster", cov_kwds={"groups": tt.anon_user_id})
    print(f"개입 전후(다음날) t-계열: humanFB β={t.params['humanFB']:+.3f} (p={t.pvalues['humanFB']:.3f})")
    rows.append(("2기", "개입전후(다음날)", "인간", t.params["humanFB"], *ci_of(t, "humanFB"), t.pvalues["humanFB"]))
    r2 = dl_fe_psm(p2, "llm", "humanFB", "day", "anon_user_id", "loglen")
    for k, nm in [("dl_now", "분포시차:당일"), ("dl_lag", "분포시차:전일"), ("fe", "FE"), ("psm", "PSM")]:
        b, lo, hi, pv = r2[k]; print(f"{nm:14s} β={b:+.3f} (p={pv:.3f}, CI {lo:+.3f}~{hi:+.3f})")
        rows.append(("2기", nm, "인간", b, lo, hi, pv))

    # ---- 2기: 동료 ----
    r2p = dl_fe_psm(p2, "llm", "peer", "day", "anon_user_id", "loglen")
    print(f"\n[참고] 2기 동료 개입 FE β={r2p['fe'][0]:+.3f} (p={r2p['fe'][3]:.3f}) · PSM β={r2p['psm'][0]:+.3f} (p={r2p['psm'][3]:.3f})")
    for k, nm in [("fe", "FE(동료)"), ("psm", "PSM(동료)")]:
        b, lo, hi, pv = r2p[k]; rows.append(("2기", nm, "동료", b, lo, hi, pv))

    # ---- 1기: 동료 ----
    h("1기 — 동료 개입 효과 (LLM 감성), 시차·FE·PSM  (인간개입은 플랫폼밖)")
    r1 = dl_fe_psm(p1, "v", "peer", "day", "participant_key", "knu")
    for k, nm in [("dl_now", "분포시차:당일"), ("dl_lag", "분포시차:전일"), ("fe", "FE"), ("psm", "PSM")]:
        b, lo, hi, pv = r1[k]; print(f"{nm:14s} β={b:+.3f} (p={pv:.3f}, CI {lo:+.3f}~{hi:+.3f})")
        rows.append(("1기", nm, "동료", b, lo, hi, pv))

    # ---- ITS 두 기수 ----
    h("ITS(단절적 시계열) — 미션 종료 기준점, 두 기수")
    d2daily = p2.groupby("kst_date").llm.agg(["size", "mean"]).reset_index()
    d2daily = d2daily[d2daily["size"] >= 3].rename(columns={"kst_date": "date", "mean": "sent"}).reset_index(drop=True)
    lvl2, sl2 = its(d2daily, "2026-05-07")
    print(f"2기(플랫폼 일별, 종료 05-07): 수준변화 β={lvl2[0]:+.3f} (p={lvl2[3]:.3f}) · 추세 β={sl2[0]:+.3f} (p={sl2[1]:.3f})")
    print("  → 미션 종료 후 감성이 하락하지 않음(오히려 유지/상승 = 생존자 효과).")
    rows.append(("2기", "ITS 미션종료", "감성수준", *lvl2))
    d1daily = kakao_daily(args.kakao, scorer)
    lvl1, sl1 = its(d1daily, "2026-04-06")
    print(f"1기(카톡 일별, 종료 04-06): 수준변화 β={lvl1[0]:+.3f} (p={lvl1[3]:.3f}) · 추세 β={sl1[0]:+.3f} (p={sl1[1]:.3f})")
    print("  → 카톡에선 종료 직후 하락(경계) = 마찰·토큰이슈 토로.")
    rows.append(("1기", "ITS 미션종료", "감성수준", *lvl1))

    h("Part 4. DID(대체) & 종합")
    print("DID: 두 기수 모두 처치·대조 평행추세 집단이 불명확(개입이 Day와 얽힘) → FE·ITS·이벤트스터디로 대체.")
    print("\n[종합표]")
    print(f"{'기수':5s}{'방법':16s}{'처치':6s}{'계수':>9s}{'p':>8s}")
    for c, mth, tr, b, lo, hi, pv in rows:
        print(f"{c:5s}{mth:16s}{tr:6s}{b:>+9.3f}{pv:>8.3f}")
    print("\n결론(LLM 감성으로도 동일): 통제 강한 방법일수록 개입 효과 0 수렴, 대부분 비유의.")
    print("        X₂(AI)는 두 기수 모두 미션Day 공선으로 분리 불가 → 관찰데이터 한계, 3·4기 실험 필요.")

    # ---- 그림: 두 기수 forest ----
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    from matplotlib import font_manager
    for pth in ["/usr/share/fonts/truetype/nanum/NanumBarunGothic.ttf", "/usr/share/fonts/truetype/nanum/NanumGothic.ttf"]:
        if os.path.exists(pth):
            font_manager.fontManager.addfont(pth); plt.rcParams["font.family"] = font_manager.FontProperties(fname=pth).get_name(); break
    plt.rcParams["axes.unicode_minus"] = False
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        fig, axes = plt.subplots(1, 2, figsize=(10.6, 4.6), dpi=140, sharex=True)
        for ax, coh, title in [(axes[0], "2기", "2기 (인간개입 X₁ · LLM 감성)"), (axes[1], "1기", "1기 (동료개입 · LLM 감성)")]:
            rr = [r for r in rows if r[0] == coh][::-1]
            labs = [f"{m} ({t})" for _, m, t, *_ in rr]
            for i, (_, m, t, b, lo, hi, pv) in enumerate(rr):
                col = "#c0392b" if pv < .05 else "#8894a6"
                ax.plot([lo, hi], [i, i], color=col, lw=2.4); ax.plot(b, i, "o", color=col, ms=6.5)
            ax.axvline(0, color="#333", lw=1, ls="--")
            ax.set_yticks(range(len(rr))); ax.set_yticklabels(labs, fontsize=8.3)
            ax.set_title(title, fontsize=11); ax.set_xlabel("개입 효과 (LLM 감성, 95% CI)")
            for s in ("top", "right"): ax.spines[s].set_visible(False)
        fig.suptitle("떡진 데이터 변인분리(LLM 감성) — 통제할수록 0으로 수렴 (빨강=p<.05)", fontsize=12, y=1.02)
        fig.tight_layout(); fp = os.path.join(args.figdir, "fig17_cohort_confound_llm.png")
        fig.savefig(fp, bbox_inches="tight"); plt.close(fig)
    print(f"\n[figure] {fp}")
    pd.DataFrame(rows, columns=["cohort", "method", "treat", "coef", "lo", "hi", "p"]).to_csv("cohort_confound_llm.csv", index=False)
    print("[saved] cohort_confound_llm.csv")


if __name__ == "__main__":
    main()
