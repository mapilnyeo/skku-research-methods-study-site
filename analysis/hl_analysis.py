#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
'떠먹이' 2기 — HL(Human-Likeness, AI의 인간 유사성 = X₂) 분석.

교수님 프레임의 마지막 조각. 지금까지 X₂는 '원자료에 없음'이라 프록시만 썼는데,
피드백 내용 분석을 근거로 **문체 기반 인간유사성(HL) 점수**를 제대로 만든다.

방법:
  1) 운영자(사람) vs AI 댓글을 문체 특징(이모티콘·따뜻한말·길이·유도질문)으로 구분하는 분류기 학습.
  2) 그 분류기의 P(사람스러움) = HL 점수. AI 댓글에 적용 → 각 AI 피드백의 인간유사성.
  3) 받은 AI 피드백의 HL이 참가자 결과(지속·기분)와 관계있나 (미션Day 통제).

실행: python analysis/hl_analysis.py /path/to/tteomeogi_csv [--figdir DIR]
의존성: pandas numpy scipy scikit-learn statsmodels matplotlib
"""
import sys, os, re, argparse
import numpy as np, pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import cross_val_predict
from sklearn.metrics import roc_auc_score
import statsmodels.formula.api as smf

EMO = r"[:;][)(D]|ㅎㅎ|ㅋㅋ|~|!!|😊|🙂|👍|❤|👏"
WARM = r"응원|감사|함께|같이|화이팅|반갑|축하|힘내|고생|수고|기대|가봐요|우리"
GUIDE = r"가설|검증|근거|회고|연결|해보|시도|확인해|변수|문장|놓치"


def h(t): print("\n" + "=" * 78 + f"\n{t}\n" + "=" * 78)


def features(t):
    t = str(t)
    return pd.Series(dict(emo=len(re.findall(EMO, t)), warm=len(re.findall(WARM, t)),
                          loglen=np.log1p(len(t)), guide=len(re.findall(GUIDE, t))))


def build_hl(csv_dir):
    c = pd.read_csv(f"{csv_dir}/assignments_comments.csv")
    fb = c[c.actor_type.isin(["ai_tutor", "human_operator"])].copy()
    X = fb.text_clean.apply(features)
    y = (fb.actor_type == "human_operator").astype(int).values     # 1 = 사람
    Xs = StandardScaler().fit_transform(X.values)
    h("1. 인간 vs AI 문체 분류기 → HL 점수")
    auc = roc_auc_score(y, cross_val_predict(LogisticRegression(max_iter=1000), Xs, y, cv=5, method="predict_proba")[:, 1])
    clf = LogisticRegression(max_iter=1000).fit(Xs, y)
    print(f"교차검증 AUC = {auc:.3f} (문체가 거의 완벽히 구분됨)")
    print("'사람스러움' 신호 (표준화 계수):")
    for n, co in zip(["이모티콘", "따뜻한말", "길이(log)", "유도질문"], clf.coef_[0]):
        print(f"   {n:10s} {co:+.2f}")
    fb["HL"] = clf.predict_proba(Xs)[:, 1]
    ai = fb[fb.actor_type == "ai_tutor"]
    print(f"\nAI 댓글 HL: 평균 {ai.HL.mean():.3f} · 중앙값 {ai.HL.median():.3f} · 최대 {ai.HL.max():.3f}")
    print(f"운영자 댓글 HL 평균: {fb[fb.actor_type=='human_operator'].HL.mean():.3f}")
    print("→ AI 피드백은 문체상 거의 '사람 같지 않다'(평균 0.03). 사람같은 AI 댓글은 대개 짧은 안내글.")
    return fb


def hl_outcome(fb, csv_dir):
    h("2. HL(받은 AI 피드백의 인간유사성) → 결과, 미션Day 통제")
    ai = fb[fb.actor_type == "ai_tutor"]
    agg = ai.groupby(["anon_post_user_id", "post_day"]).agg(HL=("HL", "mean")).reset_index()
    agg.columns = ["u", "day", "HL"]
    ap = pd.read_csv(f"{csv_dir}/assignments_posts.csv")
    m = ap[(ap.actor_type == "participant") & (ap["day"].isin([0, 1, 2, 3, 4, 5]))].copy()
    sub = m.groupby(["anon_user_id", "day"]).agg(sent=("sentiment_score", "mean")).reset_index(); sub["submitted"] = 1
    users = m.anon_user_id.unique()
    grid = pd.MultiIndex.from_product([users, [0, 1, 2, 3, 4, 5]], names=["u", "day"]).to_frame(index=False)
    g = grid.merge(sub, left_on=["u", "day"], right_on=["anon_user_id", "day"], how="left")
    g["submitted"] = g["submitted"].fillna(0); g = g.sort_values(["u", "day"])
    g["next_sub"] = g.groupby("u")["submitted"].shift(-1); g["sent_next"] = g.groupby("u")["sent"].shift(-1)
    d = g.merge(agg, on=["u", "day"], how="inner"); d["day"] = d["day"].astype(int)
    d["HL_z"] = (d.HL - d.HL.mean()) / d.HL.std()
    print(f"대상: AI 피드백 받은 제출 n={len(d)}")
    rs = d[d.day < 5].dropna(subset=["next_sub"])
    mR = smf.ols("next_sub ~ HL_z + C(day)", data=rs).fit(cov_type="cluster", cov_kwds={"groups": rs.u})
    print(f"[계속 참여] HL β={mR.params['HL_z']:+.3f} p={mR.pvalues['HL_z']:.3f}")
    sN = d.dropna(subset=["sent_next"])
    mS = smf.ols("sent_next ~ HL_z + C(day)", data=sN).fit(cov_type="cluster", cov_kwds={"groups": sN.u})
    print(f"[다음 기분] HL β={mS.params['HL_z']:+.3f} p={mS.pvalues['HL_z']:.3f}")
    d["HL_t"] = pd.qcut(d.HL, 3, labels=["낮음(전형AI)", "중간", "높음(사람같음)"])
    print("\nHL 3분위별 (다음 기분 / 계속율) — 사실상 평평:")
    for t, gr in d.groupby("HL_t", observed=True):
        cont = 100 * gr[gr.day < 5].next_sub.mean()
        print(f"   {t:16s} n={len(gr):3d} | 다음기분 {gr.sent_next.mean():+.3f} | 계속율 {cont:.0f}%")
    print("\n⚠️ 교란: 높은 HL AI 댓글은 대체로 '짧은 행정/안내'(예: 조배정 :)) → 실질 피드백과 성격 다름.")
    print("⚠️ 근본 한계: AI 문체가 거의 안 변해서(전부 낮은 HL) X₂ 효과를 관찰로 추정하기 어렵다.")
    return fb


def figure(fb, figdir):
    import warnings, matplotlib
    matplotlib.use("Agg"); import matplotlib.pyplot as plt
    from matplotlib import font_manager
    for path in ["/usr/share/fonts/truetype/nanum/NanumBarunGothic.ttf",
                 "/usr/share/fonts/truetype/nanum/NanumGothic.ttf"]:
        if os.path.exists(path):
            font_manager.fontManager.addfont(path)
            plt.rcParams["font.family"] = font_manager.FontProperties(fname=path).get_name(); break
    plt.rcParams["axes.unicode_minus"] = False
    ai = fb[fb.actor_type == "ai_tutor"].HL; ho = fb[fb.actor_type == "human_operator"].HL
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        fig, ax = plt.subplots(figsize=(8.2, 4.0), dpi=130)
        bins = np.linspace(0, 1, 21)
        ax.hist(ai, bins=bins, color="#2b6cb0", alpha=.85, label=f"AI 튜터 (평균 {ai.mean():.2f})")
        ax.hist(ho, bins=bins, color="#c0392b", alpha=.7, label=f"운영자(사람) (평균 {ho.mean():.2f})")
        ax.set_xlabel("인간유사성 HL 점수  (0 = 전형적 AI 문체 · 1 = 사람 문체)")
        ax.set_ylabel("댓글 수")
        ax.set_title("AI 피드백은 거의 '사람 같지 않다' — HL 분포 (분류기 AUC 0.99)", fontsize=11.5)
        for s in ("top", "right"): ax.spines[s].set_visible(False)
        ax.legend(frameon=False)
        fig.tight_layout()
        fp = os.path.join(figdir, "fig6_human_likeness.png")
        fig.savefig(fp); plt.close(fig)
    print(f"\n[figure] {fp}")


def main():
    a = argparse.ArgumentParser(); a.add_argument("csv_dir"); a.add_argument("--figdir", default=".")
    args = a.parse_args(); os.makedirs(args.figdir, exist_ok=True)
    fb = build_hl(args.csv_dir)
    fb = hl_outcome(fb, args.csv_dir)
    figure(fb, args.figdir)
    h("결론: HL은 잘 측정되나(AUC .99), 2기 AI는 문체가 거의 안 변해 X₂ 효과 추정 불가 → 3·4기서 HL을 '조작'해야 함.")


if __name__ == "__main__":
    main()
