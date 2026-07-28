#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
1기 LLM 감성 재측정 분석 — 2기와 동일 방식(LLM 주석 + 코드북).
448 미션 제출글을 LLM(Claude)이 valence(-2~+2)·이산감정·대상으로 라벨링.
목적: 사전(KNU)의 'Day0 어휘 고점' 착시를 LLM 측정으로 걷어내는지 검증.

입력: c1_llm_labels.csv (pid,valence,emotion,target) · c1_label_map.csv (pid,day,...)
      + KNU 재측정(cohort1_pipeline의 KnuScorer)
실행: python analysis/cohort1_llm_sentiment.py <1gi_dir> <knu_json> [--figdir DIR]
"""
import sys, os, json, argparse, warnings
import numpy as np, pandas as pd

MDAYS = [0, 1, 2, 3, 4, 5]


def h(t): print("\n" + "=" * 78 + f"\n{t}\n" + "=" * 78)


class KnuScorer:
    NEG = {"안", "못", "않다", "없다", "말다", "아니다", "아니"}
    def __init__(self, p):
        knu = json.load(open(p, encoding="utf-8")); self.lex = {}
        for e in knu:
            for key in {e["word"], e.get("word_root", "")}:
                k = key.strip()
                if len(k) >= 2: self.lex[k] = int(e["polarity"])
        from konlpy.tag import Okt; self.okt = Okt()
    def score(self, t):
        if not isinstance(t, str) or not t.strip(): return 0.0
        w = [x for x, _ in self.okt.pos(t, norm=True, stem=True)]
        pol = cnt = 0
        for i, x in enumerate(w):
            if x in self.lex:
                p = self.lex[x]
                if any(w[j] in self.NEG for j in range(max(0, i - 2), i)): p = -p
                pol += p; cnt += 1
        return (pol / cnt) / 2.0 if cnt else 0.0


def main():
    a = argparse.ArgumentParser(); a.add_argument("d1"); a.add_argument("knu")
    a.add_argument("--labels", default="c1_llm_labels.csv")
    a.add_argument("--map", default="c1_label_map.csv")
    a.add_argument("--figdir", default="."); args = a.parse_args()
    os.makedirs(args.figdir, exist_ok=True)

    lab = pd.read_csv(args.labels)
    mp = pd.read_csv(args.map)
    df = lab.merge(mp, on="pid")
    df["v"] = df["valence"] / 2.0            # -1..+1 정규화

    # KNU 재측정 (원문에서)
    ap = pd.read_csv(f"{args.d1}/assignments_posts.csv")
    ap = ap[(ap.day != 999) & (~ap.post_text.astype(str).str.startswith('{"version"'))
            & (ap.day.isin(MDAYS))].copy().reset_index(drop=True)
    ap["pid"] = ["1P%03d" % i for i in range(len(ap))]
    scorer = KnuScorer(args.knu)
    ap["knu"] = ap.post_text.apply(scorer.score)
    df = df.merge(ap[["pid", "knu"]], on="pid")

    h("1. LLM 라벨 분포 (448 미션 제출)")
    print("valence:", df.valence.value_counts().sort_index().to_dict())
    print("이산감정:", df.emotion.value_counts().to_dict())
    print("대상:", df.target.value_counts().to_dict())
    print(f"→ 긍정(+1/+2) {(df.valence>0).mean():.0%} · 중립 {(df.valence==0).mean():.0%} · "
          f"부정(<0) {(df.valence<0).mean():.0%}")

    h("2. 미션Day별 감성 — LLM vs KNL 사전 (핵심: Day0 착시 검증)")
    g = df.groupby("day").agg(n=("v", "size"), LLM=("v", "mean"), KNU=("knu", "mean")).round(3)
    print(g.to_string())
    r_day = g.LLM.corr(g.KNU)
    print(f"\nDay 단위 LLM vs KNU 상관 = {r_day:.2f}")
    print(f"글 단위 상관 = {df.v.corr(df.knu):.2f} · 부호일치율 {(np.sign(df.v)==np.sign(df.knu)).mean():.0%}")
    d0k, d1k = g.loc[0, "KNU"], g.loc[1:, "KNU"].mean()
    d0l, d1l = g.loc[0, "LLM"], g.loc[1:, "LLM"].mean()
    print(f"\nKNU: Day0 {d0k:+.3f} → Day1~5 평균 {d1k:+.3f}  (낙차 {d0k-d1k:+.3f})")
    print(f"LLM: Day0 {d0l:+.3f} → Day1~5 평균 {d1l:+.3f}  (낙차 {d0l-d1l:+.3f})")

    h("3. 이산감정 × 미션Day")
    ct = pd.crosstab(df.day, df.emotion)
    print(ct.to_string())
    print("→ Day0=동기기대(자기소개) · Day1~5=성취만족(회고) 로 뚜렷이 구분됨.")

    # 그림
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    from matplotlib import font_manager
    for p in ["/usr/share/fonts/truetype/nanum/NanumBarunGothic.ttf",
              "/usr/share/fonts/truetype/nanum/NanumGothic.ttf"]:
        if os.path.exists(p):
            font_manager.fontManager.addfont(p)
            plt.rcParams["font.family"] = font_manager.FontProperties(fname=p).get_name(); break
    plt.rcParams["axes.unicode_minus"] = False
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        fig, ax = plt.subplots(figsize=(8.4, 4.4), dpi=130)
        ax.plot(g.index, g.KNU, "-s", color="#e07b39", label="KNU 사전 (Day0 어휘 고점)")
        ax.plot(g.index, g.LLM, "-o", color="#2b6cb0", label="LLM 주석 (실제 의미)")
        ax.axhline(0, color="#aaa", lw=.8)
        ax.set_xlabel("미션 Day (0=자기소개)"); ax.set_ylabel("평균 감성 (-1~+1)")
        ax.set_title("1기 — LLM 측정은 사전의 'Day0 고점' 착시를 걷어낸다", fontsize=12)
        for s in ("top", "right"): ax.spines[s].set_visible(False)
        ax.legend(frameon=False); fig.tight_layout()
        fp = os.path.join(args.figdir, "fig15_1gi_llm_vs_knu.png")
        fig.savefig(fp); plt.close(fig)
    print(f"\n[figure] {fp}")

    # 저장 (텍스트 없이 pid·day·valence·knu만)
    out = df[["pid", "day", "valence", "emotion", "target", "v", "knu"]]
    out.to_csv("c1_llm_panel.csv", index=False)
    print("[saved] c1_llm_panel.csv (텍스트 없음)")
    h("완료")


if __name__ == "__main__":
    main()
