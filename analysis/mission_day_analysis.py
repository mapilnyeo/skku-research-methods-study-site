#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
'떠먹이' 2기 — 미션Day(Day0~Day5) 기준 취합·분석.

핵심 아이디어(사용자 지적):
  달력 날짜는 사람마다 다르지만(늦게 한 사람 포함) Day1~Day5의 미션 '내용'은 동일하다.
  따라서 분석 단위를 달력일이 아니라 **미션Day**로 잡으면
   - 늦게 완료한 제출도 모두 취합되고(late completion 포함),
   - '같은 내용'끼리 비교하므로 달력-시간 교란이 제거된다.

데이터:
  assignments_posts.csv 의 참가자 제출(day 0~5, JSON 아티팩트 day=999 자동 제외).
  제출별 피드백은 ai_comment_count / human_operator_comment_count 로 직접 측정.

실행: python analysis/mission_day_analysis.py /path/to/tteomeogi_csv [--figdir DIR]
의존성: pandas numpy scipy statsmodels matplotlib
"""
import sys, os, argparse
import numpy as np, pandas as pd
from scipy import stats
import statsmodels.formula.api as smf

pd.set_option("display.width", 200)
MISSION_END = pd.Timestamp("2026-05-07")


def h(t): print("\n" + "=" * 78 + f"\n{t}\n" + "=" * 78)


def load_missions(csv_dir):
    ap = pd.read_csv(f"{csv_dir}/assignments_posts.csv")
    m = ap[(ap.actor_type == "participant") & (ap["day"].isin([0, 1, 2, 3, 4, 5]))].copy()
    m["kst"] = pd.to_datetime(m["created_at_kst"])
    m["late"] = (m["kst"] > MISSION_END).astype(int)          # 미션기간 이후 제출 여부
    m["humanFB"] = (m.human_operator_comment_count > 0).astype(int)
    m["aiFB"] = (m.ai_comment_count > 0).astype(int)
    m["loglen"] = np.log1p(m.text_length)
    m = m.sort_values(["anon_user_id", "day"])
    return m


def part_aggregate(m):
    h("1. 미션Day별 취합 (달력 날짜 무관, 늦게 한 사람 포함)")
    g = m.groupby("day").agg(n=("sentiment_score", "size"), sent=("sentiment_score", "mean"),
                             sd=("sentiment_score", "std"),
                             aiFB=("aiFB", "mean"), humanFB=("humanFB", "mean"),
                             late=("late", "mean")).round(3)
    g.columns = ["n", "감성평균", "감성SD", "AI피드백율", "운영자피드백율", "미션후제출율"]
    print(g.to_string())
    print(f"\n총 제출 {len(m)}건 · 참가자 {m.anon_user_id.nunique()}명 · 미션기간 이후 제출 {int(m.late.sum())}건({100*m.late.mean():.0f}%)")
    print("→ 운영자 개입은 Day0~1에 집중, AI는 전 구간 일정 (개입이 미션Day와 강하게 얽혀 있음).")


def ontime_vs_late(m):
    h("2. 같은 미션Day 안에서 '제때' vs '늦게' 제출 비교 (내용 동일 통제)")
    rows = []
    for dd in range(6):
        s = m[m.day == dd]
        on = s[s.late == 0]["sentiment_score"]; la = s[s.late == 1]["sentiment_score"]
        if len(on) >= 3 and len(la) >= 3:
            t, p = stats.ttest_ind(on, la, equal_var=False)
            rows.append((dd, len(on), round(on.mean(), 3), len(la), round(la.mean(), 3), round(t, 2), round(p, 3)))
    out = pd.DataFrame(rows, columns=["Day", "n_제때", "감성_제때", "n_늦게", "감성_늦게", "t", "p"])
    print(out.to_string(index=False) if len(out) else "  (셀별 표본 부족)")
    print("→ 같은 내용(Day)인데 제때/늦게 감성이 비슷하면, 늦게 한 데이터도 함께 써도 된다는 근거.")


def progression_and_intervention(m):
    h("3. 미션 진행에 따른 감성 & 개입 효과 (미션Day FE + 사용자 FE)")

    # 3-A 진행 곡선: Day0 기준 대비 각 Day 감성
    print("3-A 미션Day 진행 곡선 (OLS, Day0=기준):")
    mm = m.copy(); mm["day"] = mm["day"].astype(int)
    r = smf.ols("sentiment_score ~ C(day)", data=mm).fit()
    base = r.params["Intercept"]
    print(f"  Day0 평균={base:.3f}")
    for dd in range(1, 6):
        k = f"C(day)[T.{dd}]"
        if k in r.params:
            print(f"  Day{dd}: Day0 대비 {r.params[k]:+.3f} (p={r.pvalues[k]:.3f})")

    # 3-B 미션Day 시차: Day t 피드백 → Day t+1 제출 감성 (사용자 FE + Day FE)
    print("\n3-B 미션Day 시차 회귀 — 다음 Day 제출 감성 ~ 이번 Day 피드백 (사용자+Day FE):")
    g = m.sort_values(["anon_user_id", "day"]).groupby("anon_user_id", group_keys=False)
    m2 = m.copy()
    m2["sent_next"] = g["sentiment_score"].shift(-1)
    m2["day_next"] = g["day"].shift(-1)
    m2 = m2[m2["day_next"] == m2["day"] + 1]                # 연속된 Day만
    reg = m2.dropna(subset=["sent_next"]).copy()
    reg["day"] = reg["day"].astype(int)
    model = smf.ols("sent_next ~ humanFB + aiFB + sentiment_score + loglen + C(day) + C(anon_user_id)",
                    data=reg).fit(cov_type="cluster", cov_kwds={"groups": reg.anon_user_id})
    print(f"  N(연속 Day 전이)={len(reg)} · 참가자={reg.anon_user_id.nunique()}")
    for k in ["humanFB", "aiFB", "sentiment_score"]:
        if k in model.params:
            tag = " [평균회귀]" if k == "sentiment_score" else ""
            print(f"    {k:16s} β={model.params[k]:+.3f}  p={model.pvalues[k]:.3f}{tag}")

    # 3-C 개입 전후(같은 Day 내) — 이번 Day 피드백 받은 제출 vs 아닌 제출의 '다음 Day' 감성
    print("\n3-C 개입 전후 비교 (다음 Day 감성 델타, 미션Day 통제):")
    reg["delta"] = reg["sent_next"] - reg["sentiment_score"]
    a = reg.loc[reg.humanFB == 1, "delta"]; b = reg.loc[reg.humanFB == 0, "delta"]
    if len(a) >= 5 and len(b) >= 5:
        t, p = stats.ttest_ind(a, b, equal_var=False)
        print(f"  운영자 피드백 후 Δ={a.mean():+.3f}(n={len(a)}) vs 무 Δ={b.mean():+.3f}(n={len(b)}) | t={t:.2f}, p={p:.3f}")
    print("  → 미션Day를 통제하면(같은 진행단계 비교) 개입 효과가 유지되는지 확인.")


def figure(m, figdir):
    import warnings, matplotlib
    matplotlib.use("Agg"); import matplotlib.pyplot as plt
    INK, AIC, HUM = "#1f2933", "#2b6cb0", "#c0392b"
    on = m[m.late == 0].groupby("day")["sentiment_score"].mean()
    la = m[m.late == 1].groupby("day")["sentiment_score"].mean()
    alld = m.groupby("day")["sentiment_score"].mean()
    fb = m.groupby("day")[["aiFB", "humanFB"]].mean()
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.3), dpi=130)
        ax1.plot(alld.index, alld.values, "-o", color=INK, lw=2.4, ms=6, label="All (pooled)")
        ax1.plot(on.index, on.values, "--o", color="#7a8699", lw=1.4, ms=4, label="On-time (≤5/7)")
        ax1.plot(la.index, la.values, ":o", color="#b0761f", lw=1.4, ms=4, label="Late (>5/7)")
        ax1.set_title("Sentiment by mission day (late completions pooled)", fontsize=11)
        ax1.set_xlabel("Mission day"); ax1.set_ylabel("Mean sentiment"); ax1.set_ylim(0, 1)
        ax1.legend(frameon=False, fontsize=8)
        w = 0.38
        ax2.bar(fb.index - w/2, fb.aiFB, w, color=AIC, label="AI feedback rate")
        ax2.bar(fb.index + w/2, fb.humanFB, w, color=HUM, label="Operator feedback rate")
        ax2.set_title("Feedback exposure by mission day", fontsize=11)
        ax2.set_xlabel("Mission day"); ax2.set_ylabel("Share of submissions"); ax2.set_ylim(0, 1.05)
        ax2.legend(frameon=False, fontsize=8)
        for ax in (ax1, ax2):
            for s in ("top", "right"): ax.spines[s].set_visible(False)
        fig.tight_layout()
        fp = os.path.join(figdir, "fig3_mission_day.png")
        fig.savefig(fp); plt.close(fig)
    print(f"\n[figure] {fp}")


def main():
    a = argparse.ArgumentParser(); a.add_argument("csv_dir"); a.add_argument("--figdir", default=".")
    args = a.parse_args(); os.makedirs(args.figdir, exist_ok=True)
    m = load_missions(args.csv_dir)
    part_aggregate(m)
    ontime_vs_late(m)
    progression_and_intervention(m)
    figure(m, args.figdir)
    h("완료")


if __name__ == "__main__":
    main()
