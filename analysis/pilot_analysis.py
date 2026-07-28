#!/usr/bin/env python3
"""
'떠먹이' 2기 파일럿 분석 — 감성 분석 방법론 적용 가능성 점검 스크립트.

교수님 제안(관찰 데이터 + 감성 분석 + 시차)을 실제 2기 데이터에 적용해
(1) 순진한 개입 전후 비교, (2) 개인·날짜 고정효과 모형, (3) 탈락(attrition) 교란,
(4) 공지 이벤트 스터디, (5) 주제별 마찰, (6) 검정력을 한 번에 확인한다.

데이터는 저장소에 포함하지 않는다(가명화된 참가자 데이터). CSV 폴더 경로만 넘겨 실행.
    python analysis/pilot_analysis.py /path/to/tteomeogi_csv

의존성: pandas, numpy, scipy, statsmodels
주의: sentiment_score는 파일럿 사전 점수이며 검증된 한국어 분류기가 아니다(측정 타당도 별도 확보 필요).
"""
import sys
import numpy as np
import pandas as pd
from scipy import stats
import statsmodels.formula.api as smf


def load_panel(csv_dir):
    p = pd.read_csv(f"{csv_dir}/student_day_panel.csv")
    p = p[p.is_admin == 0].copy()
    p["kst_date"] = pd.to_datetime(p["kst_date"])
    p = p.sort_values(["anon_user_id", "kst_date"])
    p["ai_fb"] = (p["ai_feedback_received_count"] > 0).astype(int)
    p["hu_fb"] = (p["human_feedback_received_count"] > 0).astype(int)
    p["active_next"] = p.groupby("anon_user_id")["active_any"].shift(-1)
    return p


def next_active_sentiment(active):
    """각 사용자의 '다음 활동일' 감성(비활동일은 건너뜀)."""
    def f(g):
        g = g.sort_values("kst_date")
        s = g["avg_sentiment_score"].values
        out = np.full(len(s), np.nan)
        out[:-1] = s[1:]
        return pd.Series(out, index=g.index)
    return active.groupby("anon_user_id", group_keys=False).apply(f)


def event_window(active):
    print("\n=== (1) 순진한 개입 전후 감성 델타 (교란 미통제) ===")
    d = active.dropna(subset=["delta"])
    for lab, m in [("after HUMAN fb", d.hu_fb == 1), ("no human fb", d.hu_fb == 0),
                   ("after AI fb", d.ai_fb == 1), ("no AI fb", d.ai_fb == 0)]:
        x = d.loc[m, "delta"]
        print(f"  {lab:16s} n={len(x):3d}  meanDelta={x.mean():+.3f}  meanPrev={d.loc[m,'avg_sentiment_score'].mean():.3f}")
    t, pv = stats.ttest_ind(d.loc[d.hu_fb == 1, "delta"], d.loc[d.hu_fb == 0, "delta"], equal_var=False)
    print(f"  human vs no-human: t={t:.2f}, p={pv:.3f}  (주의: 평균회귀·선택 교란)")


def fixed_effects(active):
    reg = active.dropna(subset=["sent_nextact"]).copy()
    reg["day"] = reg["kst_date"].dt.day.astype(str)
    reg["loglen"] = np.log1p(reg["event_count"])
    print(f"\n=== (2) 개인+날짜 고정효과 모형 (N={len(reg)}, users={reg.anon_user_id.nunique()}) ===")
    m = smf.ols("sent_nextact ~ hu_fb + ai_fb + avg_sentiment_score + loglen + C(anon_user_id) + C(day)",
                data=reg).fit(cov_type="cluster", cov_kwds={"groups": reg["anon_user_id"]})
    for k in ["hu_fb", "ai_fb", "avg_sentiment_score"]:
        print(f"  {k:22s} beta={m.params[k]:+.3f}  p={m.pvalues[k]:.3f}")
    print("  → 개입 계수는 고정효과 통제 후 비유의. 평균회귀(전일 감성)만 유의하면 순진한 효과는 대체로 인공물.")


def attrition(panel):
    print("\n=== (3) 탈락 교란: 피드백은 계속 참여하는 사람에게 몰린다 ===")
    a = panel.loc[panel.ai_fb == 1, "active_next"].mean()
    b = panel.loc[(panel.ai_fb == 0) & (panel.active_any == 1), "active_next"].mean()
    print(f"  P(익일 활동 | AI 피드백 받음)      = {100*a:.1f}%")
    print(f"  P(익일 활동 | 피드백 없이 활동)    = {100*b:.1f}%  → 노출이 내생적(endogenous)")


def separability(active):
    print("\n=== (4) 인간 vs AI 개입 분리 가능성 (동시발생) ===")
    ct = pd.crosstab(active.ai_fb.astype(bool), active.hu_fb.astype(bool))
    print(ct.to_string())
    both = int(((active.ai_fb == 1) & (active.hu_fb == 1)).sum())
    print(f"  둘 다 받은 활동일 n={both} → 상호작용항으로 분리 시도는 가능하나 표본 얇음")


def topic_friction(csv_dir):
    print("\n=== (5) 주제별 마찰 (강건한 기술 결과) ===")
    q = pd.read_csv(f"{csv_dir}/qna_posts.csv")
    for t in ["topic_install_path", "topic_claude_code_usage", "topic_file_md_submission",
              "topic_token_limit", "topic_research_workflow", "topic_error_debug"]:
        s = q[q[t] == 1]
        if len(s):
            neg = 100 * (s.sentiment_label == "negative").mean()
            print(f"  {t:28s} n={len(s):3d}  mean={s.sentiment_score.mean():+.3f}  neg={neg:.0f}%")


def power(active):
    d = active.dropna(subset=["delta"])
    sd = d["delta"].std()
    n1 = int((d.hu_fb == 1).sum()); n2 = int((d.hu_fb == 0).sum())
    mde = 2.8 * sd * np.sqrt(1 / n1 + 1 / n2)
    print(f"\n=== (6) 검정력 ===  sd(delta)={sd:.3f}  n1={n1} n2={n2}  MDE(80%)≈{mde:.3f} 감성단위")


def main():
    csv_dir = sys.argv[1] if len(sys.argv) > 1 else "."
    panel = load_panel(csv_dir)
    active = panel[panel.active_any == 1].copy()
    active["sent_nextact"] = next_active_sentiment(active)
    active["delta"] = active["sent_nextact"] - active["avg_sentiment_score"]

    print(f"non-admin 학생 패널: {panel.shape[0]} user-days | 활동일 {int(panel.active_any.sum())} | "
          f"인간피드백 노출 {int((active.hu_fb==1).sum())} | AI피드백 노출 {int((active.ai_fb==1).sum())}")
    event_window(active)
    fixed_effects(active)
    attrition(panel)
    separability(active)
    topic_friction(csv_dir)
    power(active)


if __name__ == "__main__":
    main()
