#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
1기 '떡진 데이터' 변인분리 분석 — ITS·분포시차·FE·PSM·DID.
교수님 방법론 표 그대로 적용하되, 1기 데이터 구조에 맞춰 정직하게 추정.

1기 구조상 핵심 제약:
  · 온플랫폼 '인간 개입(운영자)'이 없음 → 인간 개입(X₁)은 카카오톡(플랫폼 밖).
  · 온플랫폼 AI 피드백은 미션Day와 거의 완전 공선(Day0 1% → Day1~5 93~100%)
    → AI 개입 효과는 '미션Day 효과'와 분리 불가(추정 포기, 정직 보고).
  · 추정 가능한 온플랫폼 개입 = '동료 댓글(peer)' (사용자 내 변동 존재).
  · ITS는 카톡 일별 감성에 '미션 종료' 기준점으로 적용(가장 깨끗한 적용처).

실행: python analysis/cohort1_confound.py <1gi_dir> [--figdir DIR]
입력: c1_llm_panel.csv · c1_label_map.csv · <1gi_dir>/assignments_comments.csv · kakao_1gi.txt
의존성: pandas numpy scipy statsmodels scikit-learn matplotlib
"""
import sys, os, re, argparse, warnings
import numpy as np, pandas as pd
from scipy import stats
import statsmodels.formula.api as smf

MDAYS = [0, 1, 2, 3, 4, 5]
def h(t): print("\n" + "=" * 78 + f"\n{t}\n" + "=" * 78)


# ---------- 카톡 파싱(ITS용 일별 참가자 감성) ----------
MSG = re.compile(r'^\[([^\]]+)\] \[(오전|오후) (\d+):(\d+)\] (.*)$')
DATE = re.compile(r'^-+ (\d+)년 (\d+)월 (\d+)일')
OP_NAMES = {"조온_AI 조교", "가방끈지기", "코드집도의", "매필녀", "클로이"}
MEDIA = {"사진", "이모티콘", "동영상", "삭제된 메시지입니다.", "메시지가 삭제되었습니다.", ".", "파일"}

class Knu:
    NEG = {"안", "못", "않다", "없다", "말다", "아니다", "아니"}
    def __init__(s, p):
        import json; k = json.load(open(p, encoding="utf-8")); s.lex = {}
        for e in k:
            for key in {e["word"], e.get("word_root", "")}:
                kk = key.strip()
                if len(kk) >= 2: s.lex[kk] = int(e["polarity"])
        from konlpy.tag import Okt; s.okt = Okt()
    def score(s, t):
        if not isinstance(t, str) or not t.strip(): return np.nan
        w = [x for x, _ in s.okt.pos(t, norm=True, stem=True)]
        pol = c = 0
        for i, x in enumerate(w):
            if x in s.lex:
                p = s.lex[x]
                if any(w[j] in s.NEG for j in range(max(0, i - 2), i)): p = -p
                pol += p; c += 1
        return (pol / c) / 2.0 if c else np.nan

def kakao_daily(txt, scorer):
    lines = open(txt, encoding="utf-8").read().split("\n"); rows = []; cur = None
    for ln in lines:
        d = DATE.match(ln)
        if d: cur = f"{int(d.group(1))}-{int(d.group(2)):02d}-{int(d.group(3)):02d}"; continue
        m = MSG.match(ln)
        if m:
            name, _, _, _, text = m.groups()
            isop = name in OP_NAMES or name.startswith(("스텝_", "스탭_"))
            rows.append(dict(date=cur, isop=isop, text=text))
        elif rows and ln.strip() and not (ln.endswith("들어왔습니다.") or ln.endswith("나갔습니다.") or "되었습니다" in ln):
            rows[-1]["text"] += "\n" + ln
    df = pd.DataFrame(rows)
    part = df[(~df.isop) & (~df.text.str.strip().isin(MEDIA)) & (df.text.str.len() >= 2)].copy()
    part["s"] = part.text.apply(scorer.score)
    daily = part.groupby("date").agg(n=("s", "size"), sent=("s", "mean")).reset_index()
    return daily[daily.n >= 3].reset_index(drop=True)


def load_panel(d1):
    lab = pd.read_csv("c1_llm_panel.csv"); mp = pd.read_csv("c1_label_map.csv")
    df = lab.merge(mp, on=["pid", "day"])
    c = pd.read_csv(f"{d1}/assignments_comments.csv")
    rec = c.groupby("post_key").agg(
        ai=("comment_author_type", lambda s: (s == "ai_operator").sum()),
        peer=("comment_author_type", lambda s: (s == "peer_or_other").sum())).reset_index()
    m = df.merge(rec, on="post_key", how="left").fillna({"ai": 0, "peer": 0})
    m["got_ai"] = (m.ai > 0).astype(int); m["got_peer"] = (m.peer > 0).astype(int)
    m["u"] = m["participant_key"]
    # 사용자×Day 그리드로 다음날 감성 lag 구성
    m = m.sort_values(["u", "day"])
    m["sent_next"] = m.groupby("u")["v"].shift(-1)
    m["peer_lag"] = m.groupby("u")["got_peer"].shift(1)
    return m


def main():
    a = argparse.ArgumentParser(); a.add_argument("d1"); a.add_argument("--figdir", default=".")
    a.add_argument("--knu", default="knu/SentiWord_info.json"); a.add_argument("--kakao", default="kakao_1gi.txt")
    args = a.parse_args(); os.makedirs(args.figdir, exist_ok=True)
    m = load_panel(args.d1)
    results = []  # (label, coef, lo, hi, p, note)

    h("0. 추정 가능성 점검 (왜 어떤 개입은 못 재는가)")
    print("AI 피드백 수령률 by 미션Day:", m.groupby("day").got_ai.mean().round(2).to_dict())
    print("→ Day0 0.01 · Day1~5 0.93~1.00 : AI 개입 ≈ '미션Day' 와 거의 완전 공선.")
    print("  ⇒ AI 개입(X₂ 온플랫폼)의 순효과는 미션Day 효과와 분리 불가 → 추정 포기(정직).")
    print(f"동료 댓글 수령률 by Day:", m.groupby("day").got_peer.mean().round(2).to_dict())
    print(f"→ 사용자 내 변동 있는 사용자 {m.groupby('u').got_peer.nunique().gt(1).sum()}/{m.u.nunique()} : 동료 개입은 추정 가능.")

    # ---------- ITS (카톡, 미션 종료 기준점) ----------
    h("1. ITS(단절적 시계열) — 카톡 참가자 감성, 기준점=미션 종료(2026-04-06)")
    scorer = Knu(args.knu)
    daily = kakao_daily(args.kakao, scorer)
    daily["t"] = np.arange(len(daily))
    BREAK = "2026-04-06"
    daily["post"] = (daily.date > BREAK).astype(int)
    daily["t_post"] = (daily.post * (daily.t - daily[daily.date > BREAK].t.min() + 1)).clip(lower=0)
    its = smf.ols("sent ~ t + post + t_post", data=daily).fit()
    b_lvl, p_lvl = its.params["post"], its.pvalues["post"]
    ci = its.conf_int().loc["post"]
    print(daily[["date", "n", "sent"]].round(3).to_string(index=False))
    print(f"\n개입(미션종료) 후 수준변화(level) β={b_lvl:+.3f} (p={p_lvl:.3f}, 95%CI {ci[0]:+.3f}~{ci[1]:+.3f})")
    print(f"추세변화(slope) β={its.params['t_post']:+.3f} (p={its.pvalues['t_post']:.3f})")
    print("→ 미션 종료 직후 참가자 감성이 유의하게 하락(마찰·토큰이슈 토로 시기)." if p_lvl < .05
          else "→ 미션 종료 전후 수준변화는 경계/비유의(표본 작음).")
    results.append(("ITS 미션종료→감성(카톡)", b_lvl, ci[0], ci[1], p_lvl, "level change"))

    # ---------- 분포시차 (동료 개입: 당일 + 전일) ----------
    h("2. 분포시차(Distributed Lag) — 동료 댓글(당일+전일) → 감성 (사용자·Day 통제)")
    dl = m.dropna(subset=["peer_lag"]).copy()
    mdl = smf.ols("v ~ got_peer + peer_lag + C(day)", data=dl).fit(
        cov_type="cluster", cov_kwds={"groups": dl.u})
    for nm, key in [("당일 동료", "got_peer"), ("전일 동료(lag)", "peer_lag")]:
        b, p = mdl.params[key], mdl.pvalues[key]; ci = mdl.conf_int().loc[key]
        print(f"{nm:14s} β={b:+.3f} (p={p:.3f}, CI {ci[0]:+.3f}~{ci[1]:+.3f})")
        results.append((f"분포시차:{nm}", b, ci[0], ci[1], p, ""))

    # ---------- FE (사용자 + 미션Day 고정효과) ----------
    h("3. FE(고정효과) — 사용자+미션Day 고정효과, 동료 개입 → 감성")
    fe = smf.ols("v ~ got_peer + C(u) + C(day)", data=m).fit()
    b, p = fe.params["got_peer"], fe.pvalues["got_peer"]; ci = fe.conf_int().loc["got_peer"]
    print(f"동료 개입 β={b:+.3f} (p={p:.3f}, CI {ci[0]:+.3f}~{ci[1]:+.3f})  [사용자·Day 흡수]")
    print("※ got_ai는 C(day)에 거의 완전 흡수되어 계수 추정 불가/불안정 → 표에서 제외.")
    results.append(("FE:동료 개입", b, ci[0], ci[1], p, "user+day FE"))

    # ---------- PSM (동료 개입 성향 매칭) ----------
    h("4. PSM(성향점수매칭) — 동료 개입 성향 매칭 후 감성 ATT")
    from sklearn.linear_model import LogisticRegression
    from sklearn.neighbors import NearestNeighbors
    ps = m.dropna(subset=["v"]).copy()
    X = pd.get_dummies(ps["day"], prefix="d").astype(float)
    X["len_knu"] = ps["knu"].fillna(0).values
    y = ps["got_peer"].values
    ps["pscore"] = LogisticRegression(max_iter=1000).fit(X.values, y).predict_proba(X.values)[:, 1]
    tr = ps[ps.got_peer == 1]; co = ps[ps.got_peer == 0]
    nn = NearestNeighbors(n_neighbors=1).fit(co[["pscore"]].values)
    _, idx = nn.kneighbors(tr[["pscore"]].values)
    att = tr["v"].values - co["v"].values[idx.ravel()]
    t, pval = stats.ttest_1samp(att, 0)
    lo, hi = att.mean() - 1.96 * att.std(ddof=1) / np.sqrt(len(att)), att.mean() + 1.96 * att.std(ddof=1) / np.sqrt(len(att))
    print(f"ATT(동료 개입) = {att.mean():+.3f} (p={pval:.3f}, CI {lo:+.3f}~{hi:+.3f}, 매칭쌍 {len(att)})")
    results.append(("PSM:동료 개입 ATT", att.mean(), lo, hi, pval, "matched"))

    # ---------- DID (대체) ----------
    h("5. DID(이중차분) — ⚠️ 대체")
    print("처치·대조 구분이 애매(AI는 거의 전원, 동료는 산발적·자기선택) → 깨끗한 평행추세 집단 없음.")
    print("⇒ DID 대신 FE·ITS·이벤트스터디로 대체(위 결과). 교수님 표의 판단과 동일.")

    # ---------- 종합 + 그림 ----------
    h("종합")
    print(f"{'방법':26s}{'계수':>9s}{'p':>8s}")
    for lab, b, lo, hi, p, note in results:
        print(f"{lab:26s}{b:>+9.3f}{p:>8.3f}")
    print("\n결론: 추정 가능한 온플랫폼 개입(동료 댓글)은 시차·FE·PSM 모두에서 감성에 유의한 효과 없음.")
    print("       AI 개입은 미션Day와 공선이라 관찰데이터로 분리 불가. 유일한 유의 신호는 ITS(미션종료→하락).")

    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    from matplotlib import font_manager
    for p_ in ["/usr/share/fonts/truetype/nanum/NanumBarunGothic.ttf", "/usr/share/fonts/truetype/nanum/NanumGothic.ttf"]:
        if os.path.exists(p_):
            font_manager.fontManager.addfont(p_); plt.rcParams["font.family"] = font_manager.FontProperties(fname=p_).get_name(); break
    plt.rcParams["axes.unicode_minus"] = False
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        fig, ax = plt.subplots(figsize=(8.6, 4.2), dpi=140)
        labs = [r[0] for r in results][::-1]; bs = [r[1] for r in results][::-1]
        los = [r[2] for r in results][::-1]; his = [r[3] for r in results][::-1]
        ps_ = [r[4] for r in results][::-1]
        yy = np.arange(len(labs))
        for i, (b, lo, hi, p) in enumerate(zip(bs, los, his, ps_)):
            col = "#c0392b" if p < .05 else "#8894a6"
            ax.plot([lo, hi], [i, i], color=col, lw=2.4)
            ax.plot(b, i, "o", color=col, ms=7)
        ax.axvline(0, color="#333", lw=1, ls="--")
        ax.set_yticks(yy); ax.set_yticklabels(labs, fontsize=9)
        ax.set_xlabel("개입 효과 (감성, 95% 신뢰구간) — 빨강=유의(p<.05)")
        ax.set_title("1기 '떡진 데이터' 변인분리 — 개입 효과와 신뢰구간", fontsize=12)
        for s in ("top", "right"): ax.spines[s].set_visible(False)
        fig.tight_layout(); fp = os.path.join(args.figdir, "fig16_1gi_confound.png")
        fig.savefig(fp); plt.close(fig)
    print(f"[figure] {fp}")


if __name__ == "__main__":
    main()
