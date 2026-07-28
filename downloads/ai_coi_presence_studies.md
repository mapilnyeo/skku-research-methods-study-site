# AI 에이전트·챗봇 대상 CoI 프레젠스 측정 선행연구

> **랩미팅 정리 · 문헌 서베이 (구체판)**
> AI 코치/챗봇/펫다고지컬 에이전트를 대상으로 **Community of Inquiry(CoI) presence(social·cognitive·teaching)** 를 측정한 실증연구.
> 각 논문: 연도·저자·표본·측정방식·저널 등급.
> ※ 저널 등급은 JCR/SJR 기준이며 매년 변동 — 대략적 tier로 표기.

---

## 핵심 요약 표

| # | 저자 (연도) | 저널 · 등급 | 표본 | 측정 방식 | 핵심 결과 |
|---|---|---|---|---|---|
| **①** | Wang, Pang, Wallace, Wang & Chen (2024) | *Computer Assisted Language Learning* 37(4), 814–840 · **SSCI Q1, CALL 분야 대표(최상위)** | 초등 L2 학습자 **327명**(중국), AI 영어코치 | **자기보고 CoI presence 설문**(social·cognitive·teaching) + AI 사용로그 + 실제 학습성과 → 위계적 회귀 | cognitive presence·AI 외형 호감이 L2 즐거움/성과를 **정(+)** 예측. **teaching presence는 성과를 *음(−)*** 예측(반직관) |
| **②** | Li, Wu & Chiu (2025) | *Journal of Research on Technology in Education* (JRTE) · **SSCI Q1(상위)** | 대학생 **60명**(교사존재 30 vs 부재 30), 준실험 | **순차적 설명 혼합설계** — 참여도(정서·행위주도·행동·인지) 척도 + teaching presence 역할 6종 질적 분석 | teaching presence 조건이 **정서·행위주도 engagement 유의하게↑**, 행동·인지 engagement는 유사 |
| **③** | Xu, Lin, Gorter, Schneider, Weidlich, Davis, Kreijns & de Groot (2026) | *British Journal of Educational Technology* (BJET) 57, 227–242 · **SSCI Q1, ed-tech 대표(최상위)** | 초등 학습자, 실험(애니메이션 에이전트 vs 음성만) | **social presence 척도** + 학습수행 검사 → 매개분석 | 애니메이션 에이전트가 **social presence는 유발**하나 **학습성과엔 효과 없음**, 매개도 미성립 |
| **④** | Huang, Chen & Hu (2025) | *Frontiers in Psychology* 16 · **SSCI Q1~Q2(중상위)** | 대학생 **530명**(중국, AI 구술영어) | **자기보고 SEM** — 지각된 usability·presence·감성지능(EI)·의사소통의지(WTC)·L2 성장마인드셋 | presence가 성장마인드셋에 **직접 정(+)** + EI·WTC 통한 **이중매개** |
| **⑤** | Wang, Zhao, Shen & Chen (2021) | *Frontiers in Psychology* 12:694386 · **SSCI Q1~Q2(중상위)** | 온라인학습 경험 대학생 **408명**(중국) | **teaching presence 측정도구 개발** — 5요인(설계·조직 / 담화촉진 / 직접교수 / 평가 / 기술지원), EFA·CFA | teaching presence "측정 합의 부재" 문제에 대응하는 **검증된 5요인 척도** 제시 |

---

## 보조: 리뷰·파일럿 (단행본 챕터, 저널 아님)

| # | 문헌 (연도) | 형태 | 내용 |
|---|---|---|---|
| ⑥ | *Enhancing Online Learning: A Systematic Review on Integrating GenAI Chatbots into the CoI Framework* (2024, Springer) | 편저 챕터(체계적 리뷰) | GenAI 챗봇이 3 presence를 어떻게 강화하는지 종합. 측정 대부분 **자기보고 설문**, teaching presence 측정 **합의 부재** 지적 |
| ⑦ | *GenAI Chatbots as Agents in a Community of Inquiry* (2024, Springer) | 편저 챕터(파일럿) | 챗봇이 cognitive·social·teaching presence **세 축 모두에 기여** 확인 |

---

## 측정 방식 관점 정리

- **지배적 방식 = 자기보고 설문**(①④⑤⑥). CoI presence를 학습자 지각으로 리커트 측정.
- **실험/준실험**으로 presence를 조작한 사례(②③)도 있으나 표본이 작거나(②=60) 성과효과 미검출(③).
- **teaching presence 측정도구는 아직 미정립** → ⑤가 5요인 척도로 이 빈틈을 겨냥.
- **텍스트(발화·피드백 원문) 기반 객관 코딩**으로 AI presence를 측정한 연구는 **희소** (ENA 계열 일부 예외).

---

## 떠먹이 연구 함의

| 관찰 | 우리 연구의 위치 |
|---|---|
| AI×CoI 측정은 **자기보고 설문**이 주류 | 우리는 **실제 AI/운영자 피드백 텍스트를 LLM으로 객관 측정** → 방법론적 차별점 |
| ①: **teaching presence가 성과를 음(−)** 예측 | "AI가 선생님처럼/사람처럼 개입"이 항상 +가 아님 → 우리 **인간유사성(HL)×감성** 분석과 직접 연결 |
| teaching presence **측정 합의 부재**(⑤⑥) | 우리 피드백-내용 분석이 측정틀 논의에 기여 여지 |
| social·cognitive presence는 **분리 측정되나 강하게 공변** | 앞선 "동시 활성화" 문헌과 일치 → 순효과 분리엔 **실험설계 필요**(3·4기) |

**한 줄:** AI/챗봇에 CoI를 적용한 실증연구는 최상위 저널(CALL·BJET·JRTE)에 **분명히 존재**하나, 대부분 **자기보고 설문 기반·teaching presence 측정 미정립**. → 우리처럼 **실제 피드백 텍스트로 presence를 객관 측정**하면 빈틈을 메울 수 있고, 특히 ①의 "teaching presence 역효과" 결과는 우리 HL 가설과 직결된다.

---

### 참고문헌 (APA)
1. Wang, X., Pang, H., Wallace, M. P., Wang, Q., & Chen, W. (2024). Learners' perceived AI presences in AI-supported language learning: A study of AI as a humanized agent from community of inquiry. *Computer Assisted Language Learning, 37*(4), 814–840. https://doi.org/10.1080/09588221.2022.2056203
2. Li, Y., Wu, Y., & Chiu, T. K. F. (2025). How teacher presence affects student engagement with a generative artificial intelligence chatbot in learning designed with first principles of instruction. *Journal of Research on Technology in Education.* https://doi.org/10.1080/15391523.2025.2493942
3. Xu, K. M., Lin, L., Gorter, M., Schneider, S., Weidlich, J., Davis, R. O., Kreijns, K., & de Groot, R. (2026). Social presence: A key factor in embedding a pedagogical agent into online learning in primary education. *British Journal of Educational Technology, 57*, 227–242. https://doi.org/10.1111/bjet.70006
4. Huang, Y., Chen, H., & Hu, C. (2025). L2 growth mindset in AI-mediated language learning: Effects of perceived usability and presence of generative AI chatbots. *Frontiers in Psychology, 16.* https://doi.org/10.3389/fpsyg.2025.1700117
5. Wang, Y., Zhao, L., Shen, S., & Chen, W. (2021). Constructing a teaching presence measurement framework based on the community of inquiry theory. *Frontiers in Psychology, 12,* 694386. https://doi.org/10.3389/fpsyg.2021.694386

*(⑥⑦은 Springer 편저 단행본 챕터 — 서지 세부는 확인 후 보강 예정.)*
