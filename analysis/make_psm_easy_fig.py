import os, warnings
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
for p in ["/usr/share/fonts/truetype/nanum/NanumBarunGothic.ttf","/usr/share/fonts/truetype/nanum/NanumGothic.ttf"]:
    if os.path.exists(p):
        font_manager.fontManager.addfont(p); plt.rcParams["font.family"]=font_manager.FontProperties(fname=p).get_name(); break
plt.rcParams["axes.unicode_minus"]=False
FD="/home/user/skku-research-methods-study-site/analysis/figures"

def box(ax,x,y,w,h,text,fc,ec,fs=9.5,tc="#1a2230"):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0.02,rounding_size=0.08",
                                fc=fc,ec=ec,lw=1.4))
    ax.text(x+w/2,y+h/2,text,ha="center",va="center",fontsize=fs,color=tc)

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    fig,ax=plt.subplots(figsize=(11,6.2),dpi=140); ax.axis("off")
    ax.set_xlim(0,12); ax.set_ylim(0,10)
    ax.text(6,9.5,"성향점수매칭 = '조건이 비슷한 글끼리 1:1로 짝지어 비교'",
            ha="center",fontsize=14,fontweight="bold")

    # 헤더
    box(ax,0.6,8.1,3.6,0.7,"댓글(개입) 받은 글",  "#f8e7e4","#c0392b",11,"#c0392b")
    box(ax,4.9,8.1,2.2,0.7,"짝짓기 기준",         "#eef1f6","#c9d2e0",10,"#3a4aa8")
    box(ax,7.8,8.1,3.6,0.7,"댓글 안 받은 글",     "#eaf0f6","#2b6cb0",11,"#2b6cb0")

    # 3쌍: (개입글, 조건, 대조글, 기분차)
    pairs=[
     ("Day1 · 긴 글","같은 Day1\n비슷한 길이","Day1 · 긴 글","기분 차이 ≈ 0"),
     ("Day2 · 짧은 글","같은 Day2\n비슷한 길이","Day2 · 짧은 글","기분 차이 ≈ 0"),
     ("Day0 · 중간 글","같은 Day0\n비슷한 길이","Day0 · 중간 글","기분 차이 ≈ +0.1"),
    ]
    ys=[6.4,4.6,2.8]
    for (L,cond,R,diff),y in zip(pairs,ys):
        box(ax,0.6,y,3.6,1.1,L,"#fdf3f1","#e3a89e",10)
        box(ax,4.7,y+0.1,2.6,0.9,cond,"#ffffff","#c9d2e0",8.6,"#3a4aa8")
        box(ax,7.8,y,3.6,1.1,R,"#f0f6fc","#a9c6e3",10)
        # 화살표(양쪽 → 가운데)
        ax.add_patch(FancyArrowPatch((4.2,y+0.55),(4.7,y+0.55),arrowstyle="-",color="#bbb",lw=1.2))
        ax.add_patch(FancyArrowPatch((7.3,y+0.55),(7.8,y+0.55),arrowstyle="-",color="#bbb",lw=1.2))
        ax.text(11.75,y+0.55,diff,ha="right",va="center",fontsize=8.8,color="#555",style="italic")

    # 하단 결론
    box(ax,1.2,0.5,9.6,1.5,
        "① 이런 '짝'을 잔뜩 만든다   →   ② 각 짝의 기분 차이를 구한다   →   ③ 전부 평균낸다\n"
        "평균 ≈ 0 (거의 차이 없음)  →  '거의 0' = 댓글이 기분을 바꿨다는 증거 없음",
        "#e0f0ea","#177a5e",10.5,"#12684f")
    fig.tight_layout()
    fp=f"{FD}/fig23_psm_easy.png"; fig.savefig(fp,bbox_inches="tight"); plt.close(fig)
print("saved",fp)
