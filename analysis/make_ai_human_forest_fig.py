import os, warnings
import numpy as np
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from matplotlib import font_manager
for p in ["/usr/share/fonts/truetype/nanum/NanumBarunGothic.ttf","/usr/share/fonts/truetype/nanum/NanumGothic.ttf"]:
    if os.path.exists(p):
        font_manager.fontManager.addfont(p); plt.rcParams["font.family"]=font_manager.FontProperties(fname=p).get_name(); break
plt.rcParams["axes.unicode_minus"]=False
FD="/home/user/skku-research-methods-study-site/analysis/figures"

# (라벨, coef, lo, hi, p, ai여부)  위→아래
rows=[
 ("2기 · 인간 개입  (FE)",     -0.102,-0.241, 0.037,0.151,False),
 ("2기 · 인간 개입  (PSM)",    -0.021,-0.080, 0.038,0.482,False),
 ("2기 · AI 개입  (FE)",       -0.131,-0.424, 0.161,0.378,True),
 ("2기 · AI 개입  (PSM)",      -0.002,-0.057, 0.053,0.940,True),
 ("1기 · AI 개입  (FE)",       -0.150,-0.334, 0.033,0.108,True),
 ("1기 · AI 개입  (PSM)",      -0.052,-0.083,-0.021,0.001,True),
]
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    fig,ax=plt.subplots(figsize=(10.6,5.4),dpi=140)
    n=len(rows)
    ax.axvspan(-0.1,0.1,color="#e8ede6",zorder=0)
    ax.axvline(0,color="#177a5e",lw=1.6,zorder=1)
    for i,(lab,b,lo,hi,p,isai) in enumerate(rows):
        y=n-1-i
        crosses=lo<=0<=hi
        col="#8894a6" if crosses else "#c0392b"
        ax.plot([lo,hi],[y,y],color=col,lw=3,solid_capstyle="round",zorder=2)
        ax.plot(b,y,"o",color=col,ms=10,zorder=3,markeredgecolor="white",markeredgewidth=1.2)
        # 판정
        if crosses: vt,vc="효과 없음","#5b6676"
        else: vt,vc="유의하나 대조군=Day0\n(진짜 효과 아님)","#a86315"
        ax.text(0.235,y,vt,fontsize=8.4,va="center",ha="left",color=vc,fontweight="bold")
    ax.set_yticks(range(n)); ax.set_yticklabels([r[0] for r in rows][::-1],fontsize=9.8)
    ax.set_ylim(-0.7,n-0.3); ax.set_xlim(-0.48,0.45); ax.set_xticks([-0.4,-0.2,0,0.2])
    ax.set_xlabel("개입이 기분에 준 효과  (LLM 감성, 95% 신뢰구간 · 0 = 효과 없음)",fontsize=10)
    ax.set_title("변인분리 — 2기 인간개입 · 2기 AI개입 · 1기 AI개입",fontsize=13.5,fontweight="bold",pad=10)
    for s in ("top","right","left"): ax.spines[s].set_visible(False)
    ax.tick_params(left=False)
    # 그룹 구분선
    for yy in [n-2.5, n-4.5]:
        ax.axhline(yy,color="#e3e3e3",lw=1)
    fig.text(0.5,-0.04,
      "[주의]  AI 개입은 Day1부터 거의 100% 참가자에게 달려서, 'AI를 안 받은 글'이 사실상 Day0(자기소개)뿐이다.\n"
      "→ AI '효과'는 실제로는 'Day0 vs 이후'의 차이와 섞여 있어(교란), 순수 AI 효과로 볼 수 없다.  인간 개입만이 비교적 깨끗하게 추정된다.",
      ha="center",fontsize=9.3,color="#1a2230",
      bbox=dict(boxstyle="round,pad=0.6",fc="#f6ecdb",ec="#e0c9a0"))
    fig.tight_layout()
    fp=f"{FD}/fig22_ai_human_forest.png"; fig.savefig(fp,bbox_inches="tight"); plt.close(fig)
print("saved",fp)
