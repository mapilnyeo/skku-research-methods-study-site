# 왜 감성 분석을 LLM(클로드)으로 했는가 — 근거

> **핵심 주장**
> 2023년 이후 감성·텍스트 라벨링 연구의 **표준은 '감성 사전'에서 'LLM 주석'으로 이동**했습니다. 특히 **한국어처럼 사전 자원이 부족한 언어**에서 LLM의 우위가 크며, 이는 *PNAS* 등 최상위 저널에서 대규모로 입증됐습니다.

---

## 1. 근거 — 최상위 저널이 말하는 것

| 논문 (저널) | 규모 | 핵심 결과 |
| --- | --- | --- |
| **Rathje et al. 2024, *PNAS*** | 47,925건 · **12개 언어** | LLM(GPT)이 감성·감정을 인간 코더와 얼마나 잘 맞추는가 = **상관 r 0.59~0.77**. 반면 **감성 사전은 r 0.20~0.30**에 그침. → LLM이 사전보다 **2~3배 정확**, 다국어에서도 성립 |
| **Gilardi et al. 2023, *PNAS*** | 6,183건 | ChatGPT가 크라우드 작업자(사람)보다 라벨링 정확도 **약 25%p 높고**, 비용은 **20배 저렴** |
| **Ziems et al. 2024, *Computational Linguistics*** | 13개 모델 × 25개 벤치마크 | LLM을 사회과학 텍스트 분석에 쓰는 표준 방법론(프롬프트·평가) 정립. 자유형 라벨링 설명은 **크라우드 정답을 능가** |
| **권순찬 외 2024, 한국컴퓨터정보학회논문지** | 한국어(영화·게임·쇼핑) | GPT-4의 **한국어 제로샷 감성분석**이 KoBERT 등 한국어 전용 모델과 **대등~우위**. → 한국어 맥락 직접 근거 |

> **한 줄 요약:** "요즘 감성분석 연구는 사전이 아니라 LLM으로 합니다"는 *PNAS* 2편·*Computational Linguistics* 1편 + 한국어 실증으로 뒷받침됩니다.

---

## 2. 왜 '감성 사전'이나 'KoBERT'가 아니라 LLM인가?

**① 감성 사전(예: KNU 사전)의 한계 — 문맥을 못 읽습니다.**
사전은 단어 하나하나의 긍/부정만 셉니다. 그래서 우리 데이터에 흔한
> "오류가 **났지만** 해결해서 **뿌듯**했다"

같은 문장을 '오류·어려움' 때문에 **부정으로 오판**합니다. Rathje(2024)가 보인 사전의 낮은 인간 일치도(r 0.2대)가 이 문제를 그대로 보여줍니다. 우리 데이터는 "고생했지만 해결해서 만족"이 대부분이라, 사전으로는 감성이 왜곡됩니다.

**② KoBERT 같은 파인튜닝 모델의 한계 — 우리 데이터에 안 맞습니다.**
KoBERT류는 **미리 라벨링된 대량의 학습 데이터**가 있어야 하고, 학습된 도메인(영화 리뷰 등)과 우리 도메인(연구챌린지 회고글)이 다릅니다. **우리에겐 학습셋이 없습니다.** 반면 LLM은 **코드북(채점 기준)만 주면 학습 없이(zero-shot) 바로** 채점합니다.

**③ LLM의 강점 — 문맥·반어·"해결 서사"를 이해합니다.**
LLM은 문장 전체의 의미를 읽어, 위 예시를 사람처럼 **긍정**으로 판단합니다. 이것이 사전 대비 r 0.2 → 0.6~0.8의 격차를 만드는 이유입니다.

---

## 3. 정직한 한계 (설득할 때 함께 제시하면 신뢰도가 올라갑니다)

LLM이 만능은 아닙니다. 이 점을 먼저 인정하는 편이 오히려 설득력 있습니다.

- **단일 주석자 문제:** 본 분석은 LLM 1개가 라벨링했습니다. 신뢰도를 확립하려면 **사람 2명이 200~300건을 독립 코딩해 LLM과 일치도(κ, 카파)를 보고**해야 합니다. → **다음 단계로 명시.**
- **세밀한 구분의 갭:** Zhang et al. 2024(*Findings of NAACL*, "A Reality Check")는 LLM이 큰 방향은 잘 잡지만 **미세한 강도·특정 대상(aspect) 감정**에선 여전히 전용 모델에 뒤질 수 있다고 경고합니다. → 우리도 강도(intensity)는 조심해서 해석.

> **따라서 우리 입장:** "LLM으로 1차 채점(빠르고 문맥 이해) → 인간 코더로 신뢰도 검증"이라는, **최신 표준을 그대로 따르는** 2단계 설계입니다.

---

## 참고문헌

1. Rathje, S., Mirea, D.-M., Sucholutsky, I., Marjieh, R., Robertson, C. E., & Van Bavel, J. J. (2024). **GPT is an effective tool for multilingual psychological text analysis.** *Proceedings of the National Academy of Sciences (PNAS)*, 121(34), e2308950121. https://doi.org/10.1073/pnas.2308950121
2. Gilardi, F., Alizadeh, M., & Kubli, M. (2023). **ChatGPT outperforms crowd workers for text-annotation tasks.** *PNAS*, 120(30), e2305016120. https://doi.org/10.1073/pnas.2305016120
3. Ziems, C., Held, W., Shaikh, O., Chen, J., Zhang, Z., & Yang, D. (2024). **Can Large Language Models Transform Computational Social Science?** *Computational Linguistics*, 50(1), 237–291. https://aclanthology.org/2024.cl-1.8/
4. 권순찬, 이동희, 장백철 (2024). **대규모 언어 모델을 사용한 제로샷 한국어 감성 분석: 사전 학습된 언어 모델과의 비교.** *한국컴퓨터정보학회논문지*, 29(2), 43–50.
5. Zhang, W., Deng, Y., Liu, B., Pan, S. J., & Bing, L. (2024). **Sentiment Analysis in the Era of Large Language Models: A Reality Check.** *Findings of NAACL 2024*. https://aclanthology.org/2024.findings-naacl.246/
