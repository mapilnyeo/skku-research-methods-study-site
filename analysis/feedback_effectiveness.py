#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
'떠먹이' 2기 — 어떤 피드백이 효과가 있었나 (방법론 + 결과).

'효과'의 대상을 3가지로 넓혀 피드백 종류(AI / 운영자 / 동료)·양·타이밍별로 분석:
  ① 계속 참여 (다음 미션Day 제출) — retention
  ② 완주 (5일 완료) — completion
  ③ 기분 (다음 제출 감성) — sentiment

핵심 설계:
  - 리스크셋을 '오늘 제출한 사람'으로 한정 → 모두 동일하게 '오늘 참여'한 상태에서 비교.
  - 피드백은 미션Day와 강하게 얽혀 있으므로(운영자=Day0 몰빵, AI=Day1+ 거의 전원) 미션Day 고정효과로 통제.
  - AI는 Day1+에서 98% 전원 → 반사실(counterfactual) 부족 → '개수(dose)'로 대신 봄.

실행: python analysis/feedback_effectiveness.py /path/to/tteomeogi_csv [--figdir DIR]
"""
import sys, os, argparse
import numpy as np, pandas as pd
import statsmodels.formula.api as smf

pd.set_option("display.width", 200)


def h(t): print("\n" + "=" * 78 + f"\n{t}\n" + "=" * 78)


def build(csv_dir):
    ap = pd.read_csv(f"{csv_dir}/assignments_posts.csv")
    m = ap[(ap.actor_type == "participant") & (ap["day"].isin([0, 1, 2, 3, 4, 5]))].copy()
    for c, src in [("ai", "ai_comment_count"), ("human", "human_operator_comment_count"), ("peer", "participant_comment_count")]:
        m[c] = (m[src] > 0).astype(int)
    users = m.anon_user_id.unique()
    grid = pd.MultiIndex.from_product([users, [0, 1, 2, 3, 4, 5]], names=["u", "day"]).to_frame(index=False)
    sub = m.groupby(["anon_user_id", "day"]).agg(
        ai=("ai", "max"), human=("human", "max"), peer=("peer", "max"),
        ai_n=("ai_comment_count", "sum"), sent=("sentiment_score", "mean")).reset_index()
    sub["submitted"] = 1
    g = grid.merge(sub, left_on=["u", "day"], right_on=["anon_user_id", "day"], how="left")
    g["submitted"] = g["submitted"].fillna(0)
    for c in ["ai", "human", "peer", "ai_n"]:
        g[c] = g[c].fillna(0)
    g = g.sort_values(["u", "day"])
    g["next_sub"] = g.groupby("u")["submitted"].shift(-1)
    return m, g


def retention(g):
    h("효과 ① 계속 참여 (다음 미션Day 제출)")
    rs = g[(g.submitted == 1) & (g.day < 5)].dropna(subset=["next_sub"]).copy()
    rs["day"] = rs["day"].astype(int)
    print(f"리스크셋(오늘 제출, day<5): {len(rs)} · 전체 계속율 {100*rs.next_sub.mean():.0f}% (천장효과)")
    print("\n원자료(교란 포함):")
    for c, l in [("ai", "AI"), ("human", "운영자"), ("peer", "동료")]:
        print(f"  {l:5s} 받음 {100*rs[rs[c]==1].next_sub.mean():.0f}% vs 안받음 {100*rs[rs[c]==0].next_sub.mean():.0f}%")
    print("\n미션Day 고정효과 통제 후 (계속참여 확률 변화, 95% CI):")
    mm = smf.ols("next_sub ~ human + ai + peer + C(day)", data=rs).fit(
        cov_type="cluster", cov_kwds={"groups": rs.u})
    coefs = {}
    for k in ["human", "ai", "peer"]:
        ci = mm.conf_int().loc[k]
        coefs[k] = (mm.params[k], ci[0], ci[1], mm.pvalues[k])
        print(f"  {k:6s} β={mm.params[k]:+.3f}  [{ci[0]:+.3f}, {ci[1]:+.3f}]  p={mm.pvalues[k]:.3f}")
    gotai = rs[rs.ai == 1]
    md = smf.ols("next_sub ~ ai_n + C(day)", data=gotai).fit(cov_type="cluster", cov_kwds={"groups": gotai.u})
    ci = md.conf_int().loc["ai_n"]
    coefs["ai_dose"] = (md.params["ai_n"], ci[0], ci[1], md.pvalues["ai_n"])
    print(f"\nAI '개수' 효과 (AI 받은 제출 n={len(gotai)}): β={md.params['ai_n']:+.4f} "
          f"[{ci[0]:+.3f},{ci[1]:+.3f}] p={md.pvalues['ai_n']:.3f}  ← 유일한 (경계) 신호")
    return coefs


def completion(g, csv_dir):
    h("효과 ② 완주 (5일 완료) — 사용자 수준")
    u = pd.read_csv(f"{csv_dir}/users.csv"); u = u[u.is_admin == 0]
    early = g[g.day.isin([0, 1])].groupby("u").agg(early_ai=("ai", "max"), early_hu=("human", "max")).reset_index()
    uu = u.merge(early, left_on="anon_user_id", right_on="u", how="left").fillna(0)
    for c, l in [("early_ai", "초기 AI"), ("early_hu", "초기 운영자")]:
        a = uu[uu[c] == 1].completed_5days.mean(); b = uu[uu[c] == 0].completed_5days.mean()
        print(f"  {l}: 받음 {100*a:.0f}% vs 안받음 {100*b:.0f}%")
    print("  ⚠️ tautological — '초기 피드백'은 '초기 제출'과 거의 동의어. 인과 아님.")


def sentiment(m):
    h("효과 ③ 기분 (다음 제출 감성) — 미션Day+사용자 고정효과")
    gg = m.sort_values(["anon_user_id", "day"]).groupby("anon_user_id", group_keys=False)
    m = m.copy()
    m["sent_next"] = gg["sentiment_score"].shift(-1); m["day_next"] = gg["day"].shift(-1)
    mm = m[m["day_next"] == m["day"] + 1].dropna(subset=["sent_next"]).copy(); mm["day"] = mm["day"].astype(int)
    res = smf.ols("sent_next ~ human + ai + peer + sentiment_score + C(day) + C(anon_user_id)", data=mm).fit(
        cov_type="cluster", cov_kwds={"groups": mm.anon_user_id})
    coefs = {}
    for k in ["human", "ai", "peer"]:
        ci = res.conf_int().loc[k]; coefs[k] = (res.params[k], ci[0], ci[1], res.pvalues[k])
        print(f"  {k:6s} β={res.params[k]:+.3f}  [{ci[0]:+.3f}, {ci[1]:+.3f}]  p={res.pvalues[k]:.3f}")
    return coefs


def figure(ret, sen, figdir):
    import warnings, matplotlib
    matplotlib.use("Agg"); import matplotlib.pyplot as plt
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 3.6), dpi=130)
        def panel(ax, data, title, unit):
            labels = list(data.keys())[::-1]
            y = range(len(labels))
            for i, k in enumerate(labels):
                b, lo, hi, p = data[k]
                col = "#c0392b" if p < 0.05 else "#7a8699"
                ax.plot([lo, hi], [i, i], color=col, lw=2)
                ax.plot(b, i, "o", color=col, ms=6)
            ax.axvline(0, color="#c7cdd4", lw=1.2, ls="--")
            ax.set_yticks(list(y)); ax.set_yticklabels(labels)
            ax.set_title(title, fontsize=11); ax.set_xlabel(unit)
            for s in ("top", "right"): ax.spines[s].set_visible(False)
        nice={"human":"Operator","ai":"AI (yes/no)","peer":"Peer","ai_dose":"AI dose (per +1)"}
        panel(ax1, {nice[k]:v for k,v in ret.items()}, "Effect on continuation", "Δ P(continue)")
        panel(ax2, {nice[k]:v for k,v in sen.items()}, "Effect on next-day sentiment", "Δ sentiment")
        fig.suptitle("Which feedback was effective?  (mission-day controlled, 95% CI)", fontsize=12, y=1.02)
        fig.tight_layout()
        fp = os.path.join(figdir, "fig4_feedback_effect.png")
        fig.savefig(fp, bbox_inches="tight"); plt.close(fig)
    print(f"\n[figure] {fp}")


def main():
    a = argparse.ArgumentParser(); a.add_argument("csv_dir"); a.add_argument("--figdir", default=".")
    args = a.parse_args(); os.makedirs(args.figdir, exist_ok=True)
    m, g = build(args.csv_dir)
    ret = retention(g)
    completion(g, args.csv_dir)
    sen = sentiment(m)
    figure(ret, sen, args.figdir)
    h("결론: 미션Day를 통제하면 어떤 피드백도 통계적으로 뚜렷한 효과 없음. 유일한 경계 신호 = AI 개수(dose).")


if __name__ == "__main__":
    main()
