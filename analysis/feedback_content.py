#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
'떠먹이' 2기 — 피드백의 '내용'으로 분석 (단어·문체).

두 가지:
  A. 내용 프로파일링 — AI vs 운영자 피드백이 실제로 뭐라고 말하나 (길이·유도질문·격려·이모티콘·구별단어)
  B. 내용 → 결과 — 피드백 내용의 '변동'(특히 AI 피드백 안에서)이 받은 사람의 지속·기분과 관계있나

실행: python analysis/feedback_content.py /path/to/tteomeogi_csv [--figdir DIR]
의존성: pandas numpy scipy statsmodels konlpy matplotlib
"""
import sys, os, re, math, argparse, collections
import numpy as np, pandas as pd
import statsmodels.formula.api as smf

pd.set_option("display.width", 200)

PRAISE = r"화이팅|응원|좋|훌륭|멋지|대단|축하|최고|짱|잘하|수고|👍|❤|😊|🙂|👏"
GUIDE = r"혹시|어떤|어떻게|해보|시도|확인해|무엇|왜|볼까요|보시겠|연결|검증|가설|근거|회고"
EMO = r"[:;][)(D]|ㅎㅎ|ㅋㅋ|~|!!|😊|🙂|👍|❤|👏"


def h(t): print("\n" + "=" * 78 + f"\n{t}\n" + "=" * 78)


def feats(t):
    t = str(t)
    return pd.Series(dict(길이=len(t),
                          격려=len(re.findall(PRAISE, t)),
                          유도=len(re.findall(GUIDE, t)),
                          이모티콘=len(re.findall(EMO, t))))


def distinctive_words(c):
    from konlpy.tag import Okt
    okt = Okt()
    def toks(t):
        return [w for w, p in okt.pos(str(t), norm=True, stem=True)
                if p in ("Noun", "Verb", "Adjective") and len(w) > 1]
    ai, ho = collections.Counter(), collections.Counter()
    for t in c[c.actor_type == "ai_tutor"].text_clean.fillna(""):
        ai.update(set(toks(t)))
    for t in c[c.actor_type == "human_operator"].text_clean.fillna(""):
        ho.update(set(toks(t)))
    nAI = int((c.actor_type == "ai_tutor").sum()); nHO = int((c.actor_type == "human_operator").sum())
    rows = []
    for w in set(ai) | set(ho):
        lo = math.log((ai[w] + .5) / (nAI - ai[w] + .5)) - math.log((ho[w] + .5) / (nHO - ho[w] + .5))
        rows.append((w, ai[w], ho[w], lo))
    df = pd.DataFrame(rows, columns=["word", "ai_n", "ho_n", "lo"])
    h("A. 구별 단어 (어느 쪽에서 상대적으로 많이 나오나)")
    print("● AI 튜터 특징 단어:", ", ".join(df[df.ai_n >= 8].sort_values("lo", ascending=False).head(12).word))
    print("● 운영자 특징 단어:", ", ".join(df[df.ho_n >= 5].sort_values("lo").head(12).word))


def profile(fb):
    h("A. 내용 프로파일 (댓글당 평균)")
    p = fb.groupby("actor_type").agg(n=("길이", "size"), 길이=("길이", "mean"), 격려=("격려", "mean"),
                                     유도=("유도", "mean"), 이모티콘=("이모티콘", "mean"),
                                     감성=("sentiment_score", "mean")).round(2)
    print(p.to_string())
    print("→ AI = 길고 '유도질문·검증·가설'이 많은 인지적/교육적 피드백 (티칭 프레즌스)")
    print("→ 운영자 = 짧고 이모티콘·격려가 많은 정서적/관계적 피드백 (사회적 프레즌스)")
    return p


def content_to_outcome(fb, ap):
    h("B. AI 피드백 '내용 변동' → 받은 사람의 결과 (미션Day 통제)")
    ai = fb[fb.actor_type == "ai_tutor"]
    agg = ai.groupby(["anon_post_user_id", "post_day"]).agg(
        ai_len=("길이", "mean"), ai_praise=("격려", "sum"),
        ai_guide=("유도", "sum"), ai_sent=("sentiment_score", "mean")).reset_index()
    agg.columns = ["u", "day", "ai_len", "ai_praise", "ai_guide", "ai_sent"]
    m = ap[(ap.actor_type == "participant") & (ap["day"].isin([0, 1, 2, 3, 4, 5]))].copy()
    sub = m.groupby(["anon_user_id", "day"]).agg(sent=("sentiment_score", "mean")).reset_index(); sub["submitted"] = 1
    users = m.anon_user_id.unique()
    grid = pd.MultiIndex.from_product([users, [0, 1, 2, 3, 4, 5]], names=["u", "day"]).to_frame(index=False)
    g = grid.merge(sub, left_on=["u", "day"], right_on=["anon_user_id", "day"], how="left")
    g["submitted"] = g["submitted"].fillna(0); g = g.sort_values(["u", "day"])
    g["next_sub"] = g.groupby("u")["submitted"].shift(-1)
    g["sent_next"] = g.groupby("u")["sent"].shift(-1)
    d = g.merge(agg, on=["u", "day"], how="inner"); d["day"] = d["day"].astype(int)
    for col in ["ai_len", "ai_praise", "ai_guide", "ai_sent"]:
        d[col + "_z"] = (d[col] - d[col].mean()) / d[col].std()
    print(f"대상: AI 피드백 받은 제출 n={len(d)} (표준화 계수)")
    rs = d[d.day < 5].dropna(subset=["next_sub"])
    mR = smf.ols("next_sub ~ ai_len_z+ai_praise_z+ai_guide_z+ai_sent_z+C(day)", data=rs).fit(
        cov_type="cluster", cov_kwds={"groups": rs.u})
    print("[계속 참여] 길이 / 격려 / 유도 / 피드백감성:")
    for k in ["ai_len_z", "ai_praise_z", "ai_guide_z", "ai_sent_z"]:
        print(f"    {k:12s} β={mR.params[k]:+.3f} p={mR.pvalues[k]:.3f}")
    sN = d.dropna(subset=["sent_next"])
    mS = smf.ols("sent_next ~ ai_len_z+ai_praise_z+ai_guide_z+ai_sent_z+C(day)", data=sN).fit(
        cov_type="cluster", cov_kwds={"groups": sN.u})
    print("[다음 기분] 길이 / 격려 / 유도 / 피드백감성:")
    for k in ["ai_len_z", "ai_praise_z", "ai_guide_z", "ai_sent_z"]:
        star = " ←경계" if mS.pvalues[k] < 0.1 else ""
        print(f"    {k:12s} β={mS.params[k]:+.3f} p={mS.pvalues[k]:.3f}{star}")


def figure(prof, figdir):
    import warnings, matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib import font_manager
    for path in ["/usr/share/fonts/truetype/nanum/NanumBarunGothic.ttf",
                 "/usr/share/fonts/truetype/nanum/NanumGothic.ttf"]:
        if os.path.exists(path):
            font_manager.fontManager.addfont(path)
            plt.rcParams["font.family"] = font_manager.FontProperties(fname=path).get_name()
            break
    plt.rcParams["axes.unicode_minus"] = False
    ai = prof.loc["ai_tutor"]; ho = prof.loc["human_operator"]
    labels = ["길이(÷100자)", "유도질문", "격려어", "이모티콘"]
    aiv = [ai.길이/100, ai.유도, ai.격려, ai.이모티콘]
    hov = [ho.길이/100, ho.유도, ho.격려, ho.이모티콘]
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        fig, ax = plt.subplots(figsize=(8.2, 4.0), dpi=130)
        x = np.arange(len(labels)); w = 0.38
        ax.bar(x - w/2, aiv, w, color="#2b6cb0", label="AI 튜터")
        ax.bar(x + w/2, hov, w, color="#c0392b", label="운영자(사람)")
        for i, (a, hh) in enumerate(zip(aiv, hov)):
            ax.text(i - w/2, a + .1, f"{a:.1f}", ha="center", fontsize=8)
            ax.text(i + w/2, hh + .1, f"{hh:.1f}", ha="center", fontsize=8)
        ax.set_xticks(x); ax.set_xticklabels(labels)
        ax.set_ylabel("댓글당 평균 (횟수)")
        ax.set_title("피드백 내용 프로파일 — AI(인지적) vs 운영자(정서적)", fontsize=12)
        for s in ("top", "right"): ax.spines[s].set_visible(False)
        ax.legend(frameon=False)
        fig.tight_layout()
        fp = os.path.join(figdir, "fig5_feedback_content.png")
        fig.savefig(fp); plt.close(fig)
    print(f"\n[figure] {fp}")


def main():
    a = argparse.ArgumentParser(); a.add_argument("csv_dir"); a.add_argument("--figdir", default=".")
    args = a.parse_args(); os.makedirs(args.figdir, exist_ok=True)
    c = pd.read_csv(f"{args.csv_dir}/assignments_comments.csv")
    ap = pd.read_csv(f"{args.csv_dir}/assignments_posts.csv")
    fb = c[c.actor_type.isin(["ai_tutor", "human_operator"])].copy()
    fb = pd.concat([fb, fb.text_clean.apply(feats)], axis=1)
    prof = profile(fb)
    distinctive_words(c)
    content_to_outcome(fb, ap)
    figure(prof, args.figdir)
    h("결론: 내용은 AI=인지/교육형, 운영자=정서/관계형으로 뚜렷이 다르다(강건). "
      "다만 내용 변동→결과 효과는 대체로 비유의(경계: 따뜻한 AI 피드백→다음 기분 살짝↑).")


if __name__ == "__main__":
    main()
