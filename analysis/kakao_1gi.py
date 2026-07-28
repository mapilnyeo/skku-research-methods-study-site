#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
'떠먹이' 1기 카카오톡 오픈채팅 감성 분석 (보너스).

이 채널이 중요한 이유: 1기의 **인간 운영자 개입(X₁)** 이 실제로 일어난 곳.
플랫폼 export엔 X₁이 안 보였는데(온플랫폼은 AI 피드백뿐), 이 카톡 로그가 바로 그
'플랫폼 밖 인간 개입'의 원자료다. → 운영자 문체(따뜻함/개인화)와 참가자 감성을 처음으로 관찰.

방법: 카톡 export 파싱 → 운영자/참가자 분류(닉네임 패턴) → 미디어/시스템 메시지 제외
      → KNU 감성 → 운영자 vs 참가자 문체·감성, 날짜별 추이.
실행: python analysis/kakao_1gi.py kakao_1gi.txt SentiWord_info.json [--figdir DIR]
"""
import sys, os, re, json, argparse, warnings
import numpy as np, pandas as pd

MSG = re.compile(r'^\[([^\]]+)\] \[(오전|오후) (\d+):(\d+)\] (.*)$')
DATE = re.compile(r'^-+ (\d+)년 (\d+)월 (\d+)일')
# 운영자/스태프 계정(참가자 닉네임은 '.../학위/전공/숫자' 패턴)
OP_NAMES = {"조온_AI 조교", "가방끈지기", "코드집도의", "매필녀", "클로이"}
OP_PREFIX = ("스텝_", "스탭_")
# 텍스트 아닌 플레이스홀더
MEDIA = {"사진", "이모티콘", "동영상", "삭제된 메시지입니다.", "메시지가 삭제되었습니다.",
         ".", "파일"}


def h(t): print("\n" + "=" * 78 + f"\n{t}\n" + "=" * 78)


def is_op(name):
    return name in OP_NAMES or name.startswith(OP_PREFIX)


def parse(path):
    lines = open(path, encoding="utf-8").read().split("\n")
    rows, cur_date = [], None
    for ln in lines:
        d = DATE.match(ln)
        if d:
            cur_date = f"{int(d.group(1))}-{int(d.group(2)):02d}-{int(d.group(3)):02d}"; continue
        m = MSG.match(ln)
        if m:
            name, ap, hh, mm, text = m.groups()
            rows.append(dict(date=cur_date, name=name, ampm=ap, text=text))
        elif rows and ln.strip() and not (ln.endswith("들어왔습니다.") or ln.endswith("나갔습니다.")
                                          or "되었습니다" in ln or "방장" in ln):
            rows[-1]["text"] += "\n" + ln            # 여러 줄 메시지 이어붙임
    df = pd.DataFrame(rows)
    df["is_op"] = df.name.apply(is_op)
    df["role"] = np.where(df.is_op, "운영자", "참가자")
    df["is_media"] = df.text.str.strip().isin(MEDIA) | df.text.str.contains(r"사진 \d+장|샵검색:|http", regex=True)
    return df


# KNU scorer (동일)
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
        if not isinstance(t, str) or not t.strip(): return np.nan, 0
        w = [x for x, _ in self.okt.pos(t, norm=True, stem=True)]
        pol = cnt = 0
        for i, x in enumerate(w):
            if x in self.lex:
                p = self.lex[x]
                if any(w[j] in self.NEG for j in range(max(0, i - 2), i)): p = -p
                pol += p; cnt += 1
        return ((pol / cnt) / 2.0, cnt) if cnt else (0.0, 0)


EMO = r"[:;][)(D]|ㅎㅎ|ㅋㅋ|~|!!|😊|🙂|👍|❤|👏|🫢|✨|🙏|😊"
WARM = r"응원|감사|함께|같이|화이팅|반갑|축하|힘내|고생|수고|기대|드림|축하|영광|파이팅"


def main():
    a = argparse.ArgumentParser(); a.add_argument("txt"); a.add_argument("knu")
    a.add_argument("--figdir", default="."); args = a.parse_args()
    os.makedirs(args.figdir, exist_ok=True)
    df = parse(args.txt)

    h("1. 카톡 채널 개요")
    print(f"총 메시지 {len(df)}건 · 참여자 {df.name.nunique()}명 "
          f"(운영자 {df[df.is_op].name.nunique()} · 참가자 {df[~df.is_op].name.nunique()})")
    print(f"기간: {df.date.min()} ~ {df.date.max()}")
    print(f"메시지 구성: 운영자 {int(df.is_op.sum())} · 참가자 {int((~df.is_op).sum())}")
    print(f"미디어/링크 등 비텍스트 제외 후 텍스트 메시지: {int((~df.is_media).sum())}건")

    txt = df[~df.is_media & df.text.str.len().ge(2)].copy()
    scorer = KnuScorer(args.knu)
    sc = txt.text.apply(lambda t: pd.Series(scorer.score(t), index=["knu", "n"]))
    txt = pd.concat([txt, sc], axis=1)

    h("2. 운영자 vs 참가자 — 감성·문체")
    for role, g in txt.groupby("role"):
        emo = g.text.str.contains(EMO, regex=True).mean()
        warm = g.text.str.contains(WARM, regex=True).mean()
        print(f"[{role}] 텍스트 {len(g)}건 · 평균 KNU {g.knu.mean():+.3f} · "
              f"평균 길이 {g.text.str.len().mean():.0f}자 · 이모티콘율 {emo:.0%} · 공감표현율 {warm:.0%}")
    part = txt[txt.role == "참가자"]
    print(f"\n참가자 감성 분포: 긍정(>0.05) {(part.knu>0.05).mean():.0%} · "
          f"중립 {((part.knu>=-0.05)&(part.knu<=0.05)).mean():.0%} · 부정(<-0.05) {(part.knu<-0.05).mean():.0%}")

    h("3. 날짜별 참가자 감성 추이 (미션 기간)")
    daily = txt[txt.role == "참가자"].groupby("date").agg(n=("knu", "size"), knu=("knu", "mean"))
    daily = daily[daily.n >= 3]
    print(daily.round(3).to_string())

    h("4. 운영자 개입(X₁) 성격 — 카톡은 '따뜻한 인간 채널'인가?")
    op = txt[txt.role == "운영자"]; pa = txt[txt.role == "참가자"]
    print(f"운영자 공감표현율 {op.text.str.contains(WARM,regex=True).mean():.0%} vs "
          f"참가자 {pa.text.str.contains(WARM,regex=True).mean():.0%}")
    print(f"운영자 이모티콘율 {op.text.str.contains(EMO,regex=True).mean():.0%} vs "
          f"참가자 {pa.text.str.contains(EMO,regex=True).mean():.0%}")
    print("샘플 운영자 메시지(따뜻함):")
    for t in op[op.text.str.contains(WARM, regex=True)].text.head(3):
        print("   -", t.replace("\n", " ")[:70])

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
        fig, ax = plt.subplots(figsize=(9, 4), dpi=130)
        ax.plot(range(len(daily)), daily.knu, "-o", color="#2b6cb0")
        ax.axhline(0, color="#aaa", lw=.8)
        ax.set_xticks(range(len(daily))); ax.set_xticklabels(daily.index, rotation=45, ha="right", fontsize=7)
        ax.set_ylabel("참가자 평균 감성 KNU"); ax.set_title("1기 카톡 채널 — 날짜별 참가자 감성", fontsize=12)
        for s in ("top", "right"): ax.spines[s].set_visible(False)
        fig.tight_layout(); fp = os.path.join(args.figdir, "fig14_kakao_1gi_sentiment.png")
        fig.savefig(fp); plt.close(fig)
    print(f"\n[figure] {fp}")
    h("완료")


if __name__ == "__main__":
    main()
