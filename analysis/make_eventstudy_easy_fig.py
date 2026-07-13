import os, warnings
import numpy as np
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from matplotlib import font_manager
for p in ["/usr/share/fonts/truetype/nanum/NanumBarunGothic.ttf","/usr/share/fonts/truetype/nanum/NanumGothic.ttf"]:
    if os.path.exists(p):
        font_manager.fontManager.addfont(p); plt.rcParams["font.family"]=font_manager.FontProperties(fname=p).get_name(); break
plt.rcParams["axes.unicode_minus"]=False
FD="/home/user/skku-research-methods-study-site/analysis/figures"

# 실제 파이프라인 출력값
h_x=[-1,0,1,2];  h_y=[0.694,0.710,0.332,0.376]
a_x=[-2,-1,0,1,2]; a_y=[0.654,0.478,0.372,0.359,0.372]

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    fig,ax=plt.subplots(figsize=(10.6,5.6),dpi=140)
    # 개입한 날 세로 띠
    ax.axvspan(-0.12,0.12,color="#f0ead9",zorder=0)
    ax.text(0,0.735,"개입한 날",ha="center",fontsize=10,color="#a86315",fontweight="bold")
    # 공통 바닥선
    ax.axhline(0.36,color="#bbb",lw=1,ls="--",zorder=1)
    ax.text(2.05,0.36,"둘 다 같은\n바닥으로",fontsize=8.6,color="#888",va="center")

    ax.plot(h_x,h_y,"-o",color="#c0392b",lw=2.8,ms=11,label="사람(운영자)이 개입한 경우",zorder=3,markeredgecolor="white",markeredgewidth=1.3)
    ax.plot(a_x,a_y,"-s",color="#2b6cb0",lw=2.8,ms=10,label="AI가 개입한 경우",zorder=3,markeredgecolor="white",markeredgewidth=1.3)

    # 주석 ①: 개입한 날 최고점
    ax.annotate("① 사람이 개입한 날,\n기분이 마침 '최고점'",xy=(0,0.710),xytext=(-1.9,0.66),
                fontsize=10,color="#c0392b",fontweight="bold",
                arrowprops=dict(arrowstyle="->",color="#c0392b",lw=1.5))
    # 주석 ②: 다음날 뚝
    ax.annotate("② 다음날 뚝 떨어짐",xy=(1,0.332),xytext=(0.75,0.44),
                fontsize=10,color="#c0392b",fontweight="bold",
                arrowprops=dict(arrowstyle="->",color="#c0392b",lw=1.5))
    # 주석 ③: 둘 다 같은 바닥
    ax.annotate("③ 인간·AI 모두 똑같은 바닥\n→ 개입 '종류'와 무관",xy=(1,0.359),xytext=(1.15,0.20),
                fontsize=10,color="#333",fontweight="bold",
                arrowprops=dict(arrowstyle="->",color="#555",lw=1.4))

    ax.set_xlim(-2.4,2.7); ax.set_ylim(0.12,0.78)
    ax.set_xticks([-2,-1,0,1,2])
    ax.set_xticklabels(["이틀 전","하루 전","개입한 날","하루 뒤","이틀 뒤"],fontsize=10)
    ax.set_ylabel("평균 기분 점수 (높을수록 긍정)",fontsize=10.5)
    ax.set_title("개입 '다음날' 기분이 떨어진 건 개입 탓일까?",fontsize=14,fontweight="bold",pad=30)
    ax.legend(frameon=False,fontsize=10.5,loc="upper right")
    for s in ("top","right"): ax.spines[s].set_visible(False)

    # 하단 결론 박스
    fig.text(0.5,-0.02,
      "결론: 개입이 기분을 낮춘 게 아니다.  기분이 '높을 때' 개입이 일어났고(특히 사람은 Day0 자기소개에 몰림),\n"
      "그 다음 자연스럽게 제자리로 돌아온 것 = 평균회귀(regression to the mean).  인간이든 AI든 똑같이 떨어지는 게 그 증거.",
      ha="center",fontsize=9.5,color="#1a2230",
      bbox=dict(boxstyle="round,pad=0.6",fc="#eef1f6",ec="#c9d2e0"))
    fig.tight_layout()
    fp=f"{FD}/fig20_eventstudy_easy.png"; fig.savefig(fp,bbox_inches="tight"); plt.close(fig)
print("saved",fp)
