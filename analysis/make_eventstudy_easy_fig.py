import os, warnings
import numpy as np
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from matplotlib import font_manager
for p in ["/usr/share/fonts/truetype/nanum/NanumBarunGothic.ttf","/usr/share/fonts/truetype/nanum/NanumGothic.ttf"]:
    if os.path.exists(p):
        font_manager.fontManager.addfont(p); plt.rcParams["font.family"]=font_manager.FontProperties(fname=p).get_name(); break
plt.rcParams["axes.unicode_minus"]=False
FD="/home/user/skku-research-methods-study-site/analysis/figures"

h_x=[-1,0,1,2];  h_y=[0.694,0.710,0.332,0.376]
a_x=[-2,-1,0,1,2]; a_y=[0.654,0.478,0.372,0.359,0.372]

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    fig=plt.figure(figsize=(11,6.6),dpi=140)
    ax=fig.add_axes([0.09,0.30,0.86,0.55])   # 메인
    # 개입 전/후 배경
    ax.axvspan(-2.4,0,color="#f3f6fb",zorder=0)
    ax.axvspan(0,2.7,color="#fbf5ee",zorder=0)
    ax.axvline(0,color="#a86315",lw=1.6,zorder=1)
    ax.text(-1.2,0.755,"◀  개입 전",ha="center",fontsize=11,color="#2b6cb0",fontweight="bold")
    ax.text(0,0.775,"개입한 날",ha="center",fontsize=10.5,color="#a86315",fontweight="bold")
    ax.text(1.35,0.755,"개입 후  ▶",ha="center",fontsize=11,color="#c0392b",fontweight="bold")
    ax.axhline(0.36,color="#bbb",lw=1,ls="--",zorder=1)
    ax.text(2.12,0.36,"같은\n바닥",fontsize=8.4,color="#888",va="center")

    ax.plot(h_x,h_y,"-o",color="#c0392b",lw=2.8,ms=11,label="사람(운영자)이 개입한 경우",zorder=3,markeredgecolor="white",markeredgewidth=1.3)
    ax.plot(a_x,a_y,"-s",color="#2b6cb0",lw=2.8,ms=10,label="AI가 개입한 경우",zorder=3,markeredgecolor="white",markeredgewidth=1.3)

    ax.annotate("① 개입한 날, 기분이\n마침 '최고점'",xy=(0,0.710),xytext=(-1.95,0.63),
                fontsize=10,color="#c0392b",fontweight="bold",arrowprops=dict(arrowstyle="->",color="#c0392b",lw=1.5))
    ax.annotate("② 다음날 뚝 떨어짐",xy=(1,0.332),xytext=(0.7,0.45),
                fontsize=10,color="#c0392b",fontweight="bold",arrowprops=dict(arrowstyle="->",color="#c0392b",lw=1.5))
    ax.annotate("③ 인간·AI 모두 같은 바닥\n→ 개입 '종류'와 무관",xy=(1,0.359),xytext=(1.2,0.18),
                fontsize=10,color="#333",fontweight="bold",arrowprops=dict(arrowstyle="->",color="#555",lw=1.4))

    ax.set_xlim(-2.4,2.7); ax.set_ylim(0.12,0.80)
    ax.set_xticks([-2,-1,0,1,2]); ax.set_xticklabels(["이틀 전","하루 전","개입한 날\n(0)","하루 뒤","이틀 뒤"],fontsize=9.5)
    ax.set_ylabel("평균 기분 점수\n(높을수록 긍정)",fontsize=10)
    ax.set_title("개입 '다음날' 기분이 떨어진 건 개입 탓일까?",fontsize=14,fontweight="bold",pad=26)
    ax.legend(frameon=False,fontsize=10,loc="center right")
    for s in ("top","right"): ax.spines[s].set_visible(False)

    # ── X축 설명(정렬 개념) 하단 인셋 ──
    axx=fig.add_axes([0.09,0.085,0.86,0.14]); axx.axis("off")
    axx.set_xlim(0,10); axx.set_ylim(0,3)
    axx.text(0.0,2.6,"📌 가로축이 뭔가요?  사람마다 '처음 도움받은 날'이 달라서, 그 날을 0으로 맞춰 겹친 뒤 평균낸 것입니다.",
             fontsize=9.6,color="#1a2230",fontweight="bold")
    axx.text(2.5,1.95,"실제 날짜 (제각각)",ha="center",fontsize=8,color="#555",style="italic")
    axx.text(8.0,1.95,"'개입한 날'을 0으로 맞춤",ha="center",fontsize=8,color="#a86315",style="italic",fontweight="bold")
    # 왼쪽: 처음 개입일이 서로 다른 위치
    demo=[("A",0.55,2.3),("B",1.20,3.3),("C",1.85,2.8)]
    for nm,y,xd in demo:
        axx.plot([1.0,4.2],[y,y],color="#d8d8d8",lw=6,solid_capstyle="round")
        axx.plot(xd,y,"o",color="#a86315",ms=8)
        axx.text(0.8,y,nm,ha="right",va="center",fontsize=8,color="#555")
    axx.annotate("",xy=(6.1,1.2),xytext=(4.6,1.2),arrowprops=dict(arrowstyle="-|>",color="#3a4aa8",lw=1.8))
    # 오른쪽: 모두 같은 위치(정렬됨)
    for nm,y,_ in demo:
        axx.plot([6.5,9.7],[y,y],color="#dde3ee",lw=6,solid_capstyle="round")
        axx.plot(8.1,y,"o",color="#a86315",ms=8)
    axx.axvline(8.1,ymin=0.12,ymax=0.82,color="#a86315",lw=1.3,ls="--")
    axx.text(8.1,0.02,"0",ha="center",fontsize=8.5,color="#a86315",fontweight="bold")

    fp=f"{FD}/fig20_eventstudy_easy.png"; fig.savefig(fp,bbox_inches="tight"); plt.close(fig)
print("saved",fp)
