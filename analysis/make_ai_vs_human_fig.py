import os, warnings
import numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from matplotlib import font_manager
for p in ["/usr/share/fonts/truetype/nanum/NanumBarunGothic.ttf","/usr/share/fonts/truetype/nanum/NanumGothic.ttf"]:
    if os.path.exists(p):
        font_manager.fontManager.addfont(p); plt.rcParams["font.family"]=font_manager.FontProperties(fname=p).get_name(); break
plt.rcParams["axes.unicode_minus"]=False
FD="/home/user/skku-research-methods-study-site/analysis/figures"

p2=pd.read_csv("llm_panel.csv")
def sc(v): return v*50+50  # -1..1 -> 0..100
# Panel A: Day1, Day2 (둘 다 충분) 인간 vs AI 평균 감성
days=[1,2]; hu=[]; ai=[]; hn=[]; an=[]
for d in days:
    s=p2[p2.day==d]
    h=s[s.humanFB==1].llm; a=s[s.aiFB==1].llm
    hu.append(sc(h.mean())); ai.append(sc(a.mean())); hn.append(len(h)); an.append(len(a))
# Panel B: 수령률 by day
lab=pd.read_csv("c1_llm_panel.csv"); mp=pd.read_csv("c1_label_map.csv")
df=lab.merge(mp,on=["pid","day"])
c=pd.read_csv("tteomeogi1gi/assignments_comments.csv")
rec=c.groupby("post_key").agg(ai=("comment_author_type",lambda s:(s=="ai_operator").sum())).reset_index()
m=df.merge(rec,on="post_key",how="left").fillna({"ai":0}); m["aiFB"]=(m.ai>0).astype(int)
ai2=p2.groupby("day").aiFB.mean()*100; hu2=p2.groupby("day").humanFB.mean()*100; ai1=m.groupby("day").aiFB.mean()*100

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    fig,(axA,axB)=plt.subplots(1,2,figsize=(12.4,5.2),dpi=140,gridspec_kw={"width_ratios":[1,1.25]})

    # ---- Panel A ----
    x=np.arange(len(days)); w=0.36
    b1=axA.bar(x-w/2,hu,w,color="#c0392b",label="사람(운영자)이 도와준 글")
    b2=axA.bar(x+w/2,ai,w,color="#2b6cb0",label="AI가 도와준 글")
    for xi,v,n in zip(x-w/2,hu,hn): axA.text(xi,v+1.5,f"{v:.0f}점\n(n={n})",ha="center",fontsize=9,color="#c0392b",fontweight="bold")
    for xi,v,n in zip(x+w/2,ai,an): axA.text(xi,v+1.5,f"{v:.0f}점\n(n={n})",ha="center",fontsize=9,color="#2b6cb0",fontweight="bold")
    axA.set_xticks(x); axA.set_xticklabels([f"Day{d}" for d in days],fontsize=11)
    axA.set_ylim(0,100); axA.set_ylabel("기분 점수 (0 부정 ~ 100 긍정)",fontsize=10)
    axA.axhline(50,color="#ccc",lw=1,ls="--")
    axA.set_title("① 같은 날엔 누가 도와줘도 기분이 같다",fontsize=12,fontweight="bold",pad=8)
    axA.text(0.5,-0.16,"※ 두 개입이 함께 있는 Day1·Day2만 비교 (Day0=사람만, Day3~5=사람 표본 없음)",
             transform=axA.transAxes,ha="center",fontsize=8.3,color="#5b6676")
    axA.legend(frameon=False,fontsize=9.5,loc="lower center",ncol=1)
    for s in ("top","right"): axA.spines[s].set_visible(False)

    # ---- Panel B ----
    dd=np.arange(6)
    axB.plot(dd,ai2.values,"-o",color="#2b6cb0",lw=2.5,ms=7,label="AI 개입 (2기)")
    axB.plot(dd,ai1.reindex(range(6)).values,"--o",color="#5a9bd4",lw=2,ms=6,label="AI 개입 (1기)")
    axB.plot(dd,hu2.values,"-o",color="#c0392b",lw=2.5,ms=7,label="사람 개입 (2기)")
    axB.axhspan(85,100,color="#eaf0f6",zorder=0)
    axB.text(2.5,92,"AI가 거의 모든 글에 달림 → '안 받은 글'이 없음",fontsize=8.8,color="#2b6cb0",ha="center",fontweight="bold")
    axB.annotate("사람 개입은\nDay0에 몰림",xy=(0,97),xytext=(1.4,70),fontsize=8.8,color="#c0392b",
                 arrowprops=dict(arrowstyle="->",color="#c0392b"))
    axB.set_xticks(dd); axB.set_xticklabels([f"Day{d}" for d in dd],fontsize=10)
    axB.set_ylim(-3,105); axB.set_ylabel("그 개입을 받은 글의 비율 (%)",fontsize=10)
    axB.set_title("② 그런데 'AI 순수 효과'는 못 가른다",fontsize=12,fontweight="bold",pad=8)
    axB.text(0.5,-0.16,"AI는 Day1부터 거의 100% → 비교할 '대조군(AI 안 받은 글)'이 없어 통계로 분리 불가",
             transform=axB.transAxes,ha="center",fontsize=8.3,color="#5b6676")
    axB.legend(frameon=False,fontsize=9,loc="center right")
    for s in ("top","right"): axB.spines[s].set_visible(False)

    fig.suptitle("인간 개입 vs AI 개입 — 기분 차이는 없고, 순수 효과는 관찰만으론 못 가른다",
                 fontsize=13.5,fontweight="bold",y=1.03)
    fig.tight_layout(w_pad=4)
    fp=f"{FD}/fig19_ai_vs_human.png"; fig.savefig(fp,bbox_inches="tight"); plt.close(fig)
print("saved",fp)
print("A day1 hu/ai:",round(hu[0]),round(ai[0]),"| day2:",round(hu[1]),round(ai[1]))
