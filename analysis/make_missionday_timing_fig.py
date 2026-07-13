import os, warnings
import numpy as np
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from matplotlib import font_manager, gridspec
for p in ["/usr/share/fonts/truetype/nanum/NanumBarunGothic.ttf","/usr/share/fonts/truetype/nanum/NanumGothic.ttf"]:
    if os.path.exists(p):
        font_manager.fontManager.addfont(p); plt.rcParams["font.family"]=font_manager.FontProperties(fname=p).get_name(); break
plt.rcParams["axes.unicode_minus"]=False
FD="/home/user/skku-research-methods-study-site/analysis/figures"

days=[0,1,2,3,4,5]
sent=[0.84,0.42,0.39,0.48,0.46,0.54]        # 참가자 감성(간이 사전)
hum =[97,43,16,4,2,2]                         # 인간 개입률(%)
ai  =[0,98,98,96,94,93]                       # AI 개입률(%)

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    fig=plt.figure(figsize=(10.8,6.8),dpi=140)
    gs=gridspec.GridSpec(2,1,height_ratios=[2.1,1.15],hspace=0.28)
    ax1=fig.add_subplot(gs[0]); ax2=fig.add_subplot(gs[1],sharex=ax1)

    # ── 위: 감성 곡선 ──
    ax1.axvspan(-0.35,0.35,color="#f0ead9",zorder=0)
    ax1.plot(days,sent,"-o",color="#177a5e",lw=3,ms=11,zorder=3,markeredgecolor="white",markeredgewidth=1.3)
    ax1.annotate("감성 최고점\n(Day0 = 자기소개)",xy=(0,0.84),xytext=(0.55,0.78),
                 fontsize=10.5,color="#177a5e",fontweight="bold",arrowprops=dict(arrowstyle="->",color="#177a5e",lw=1.5))
    ax1.annotate("그 뒤 자연스럽게 내려가\n안정 구간으로",xy=(2,0.39),xytext=(2.4,0.60),
                 fontsize=10,color="#5b6676",arrowprops=dict(arrowstyle="->",color="#888",lw=1.3))
    ax1.set_ylim(0.30,0.92); ax1.set_ylabel("참가자 평균 기분\n(높을수록 긍정)",fontsize=10)
    ax1.set_title("‘인간이 개입하면 기분이 나빠진다’처럼 보인 진짜 이유 = 개입 타이밍",fontsize=13.5,fontweight="bold",pad=12)
    for s in ("top","right"): ax1.spines[s].set_visible(False)
    plt.setp(ax1.get_xticklabels(),visible=False)

    # ── 아래: 개입률 ──
    x=np.arange(6); w=0.38
    ax2.bar(x-w/2,hum,w,color="#c0392b",label="사람(운영자) 개입률")
    ax2.bar(x+w/2,ai,w,color="#2b6cb0",label="AI 개입률")
    ax2.annotate("사람은 Day0에 몰림",xy=(0.0,97),xytext=(0.35,55),fontsize=9.5,color="#c0392b",fontweight="bold",
                 arrowprops=dict(arrowstyle="->",color="#c0392b",lw=1.3))
    ax2.annotate("AI는 Day1부터 꾸준히",xy=(3.19,96),xytext=(3.1,52),fontsize=9.5,color="#2b6cb0",fontweight="bold",
                 arrowprops=dict(arrowstyle="->",color="#2b6cb0",lw=1.3))
    ax2.set_ylim(0,112); ax2.set_yticks([0,50,100]); ax2.set_yticklabels(["0%","50%","100%"])
    ax2.set_ylabel("그 개입을\n받은 비율",fontsize=10)
    ax2.set_xticks(x); ax2.set_xticklabels([f"Day{d}"+("\n(자기소개)" if d==0 else "") for d in days],fontsize=9.5)
    ax2.set_xlabel("미션 진행 →",fontsize=10)
    ax2.legend(frameon=False,fontsize=9.5,loc="lower center",bbox_to_anchor=(0.5,1.0),ncol=2)
    for s in ("top","right"): ax2.spines[s].set_visible(False)

    fig.text(0.5,-0.03,
      "핵심: 사람 운영자는 기분이 원래 가장 높은 Day0(자기소개)에 집중 개입한다.  그 다음 기분은 자연히 내려간다(개입 탓 아님).\n"
      "→ 그래서 '사람이 개입하면 기분이 떨어진다'처럼 보이는 착시가 생긴다.  (또한 사람=Day0·AI=Day1 시작이라, 이벤트 그래프의 시작점도 달랐던 것)",
      ha="center",fontsize=9.5,color="#1a2230",
      bbox=dict(boxstyle="round,pad=0.6",fc="#eef1f6",ec="#c9d2e0"))
    fig.tight_layout()
    fp=f"{FD}/fig21_missionday_timing.png"; fig.savefig(fp,bbox_inches="tight"); plt.close(fig)
print("saved",fp)
