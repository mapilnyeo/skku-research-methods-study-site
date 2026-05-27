# 1-13주차 강의자료 상세 정리

## 빠른 결론

이 수업의 핵심은 “연구 아이디어를 검증 가능한 형태로 만들고, 그에 맞는 통계분석을 선택해 결과를 해석하는 것”이다.  
따라서 모든 주차 내용은 아래 순서로 연결된다.

1. 무엇을 알고 싶은가? → Research Question / Hypothesis
2. 무엇이 원인이고 결과인가? → IV / DV
3. 어떻게 측정할 것인가? → conceptual definition / operational definition / level of measurement
4. 누구에게 물어볼 것인가? → sampling
5. 연구가 정확한가? → reliability / validity / threats
6. 어떤 방법으로 자료를 모을 것인가? → survey / experiment
7. 어떤 통계로 분석할 것인가? → descriptive statistics / inferential statistics / t-test / correlation / chi-square

---

## Week 1. 과목 소개와 과학적 앎

### 핵심 내용

- 연구란 질문에 답하기 위해 정보와 데이터를 찾는 과정이다.
- 이 수업은 “무엇을 아는가”보다 “어떻게 아는가”를 다룬다.
- 전통적 앎의 방식은 다음 세 가지다.
  - Tenacity: 오래 지속되어 온 관습이나 전통을 근거로 믿는 것
  - Intuition: 느낌상 맞다고 생각하는 것
  - Authority: 전문가나 권위 있는 출처를 근거로 믿는 것
- 과학적 앎은 logic과 observation이 함께 있어야 한다.

### 구체 예시

- “여성은 남성보다 더 자주 웃는가?”라는 질문을 연구로 바꾸는 예시가 나온다.
- 학생증 사진에서 성별과 미소 여부를 코딩한다.
  - gender: male = 1, female = 2
  - smiling: not smiling = 0, smiling = 1
- 이후 chi-square로 성별과 미소 여부의 관계를 분석한다.

### 시험 포인트

- 과학적 연구는 단순 믿음이 아니라 논리와 관찰에 기반한다.
- 사회과학은 개인 한 명보다 집단 수준의 regularity, probabilistic pattern을 설명한다.
- variable은 속성들의 묶음이고, attribute는 변수의 구체적 값이다.

---

## Week 2. 연구설계, 인과성, 연구문제와 가설

### 핵심 내용

인과관계가 성립하려면 세 조건이 필요하다.

1. Correlation: 두 변수 사이에 관계가 있어야 한다.
2. Time order: 원인이 결과보다 먼저 일어나야 한다.
3. Nonspuriousness: 제3변수로 설명되지 않아야 한다.

연구설계 절차는 다음 순서로 진행된다.

1. 연구 목적 정의
2. 개념의 정확한 의미 명시
3. 연구방법 선택
4. 측정방법 결정
5. 연구대상/표본 결정
6. 자료수집
7. 자료처리
8. 자료분석
9. 결과 보고

### RQ와 Hypothesis

- Research Question은 질문형이다.
  - 예: Will Facebook use affect psychological well-being?
- Hypothesis는 예측 진술문이다.
  - 예: Facebook use will be positively related to psychological well-being.
- 선행연구와 이론으로 방향을 예측할 수 있으면 hypothesis를 쓴다.
- 연구가 부족해 방향을 예측하기 어려우면 RQ를 쓴다.

### Directional vs. Non-directional

- Non-directional / two-tailed:
  - “A와 B는 관계가 있다.”
  - 방향은 모른다.
- Directional / one-tailed:
  - “A가 증가하면 B가 증가한다.”
  - “A 집단이 B 집단보다 높다.”
  - 방향을 명시한다.

### IV/DV 구분

- Independent Variable: 원인 또는 예측변수
- Dependent Variable: 결과 또는 영향을 받는 변수

예시:

- Does interpersonal trust within a team improve team information sharing?
  - IV: interpersonal trust
  - DV: team information sharing
- Advertisements with celebrity endorsers improve consumers’ attitudes toward the brand.
  - IV: celebrity endorser advertisement
  - DV: brand attitude

### 시험 포인트

- 문장이 질문형이면 RQ, 진술형이면 H일 가능성이 높다.
- “increase, decrease, higher, lower, positive, negative”가 있으면 directional일 가능성이 높다.
- IV는 원인, DV는 결과다.

---

## Week 3. 측정수준, APA, 연구논문 구조

### 측정수준

1. Nominal
   - 이름/범주만 구분한다.
   - 예: gender, religion, political party
   - 숫자는 단순 라벨이다.

2. Ordinal
   - 순서가 있다.
   - 간격이 같다고 볼 수 없다.
   - 예: education level, class rank

3. Interval
   - 순서와 동일 간격이 있다.
   - 절대 0은 없다.
   - 예: Fahrenheit temperature, Likert scale로 만든 심리척도

4. Ratio
   - 순서, 동일 간격, 절대 0이 있다.
   - 예: age, income, number of hours

### 왜 중요한가

측정수준이 나중에 사용할 통계분석을 결정한다.

- Nominal/ordinal → categorical variable
- Interval/ratio → numerical variable

분석 연결:

- correlation: 두 변수가 numerical
- t-test: IV는 categorical, DV는 numerical
- chi-square: 두 변수가 categorical

### APA와 논문 구조

논문 기본 구조:

1. Title page
2. Abstract
3. Introduction
4. Method
5. Results
6. Discussion
7. References

Introduction은 문제의 중요성, 선행연구, 연구목적을 설명하고 RQ/H로 끝난다.  
Method는 participants, procedures, measures를 설명한다.  
Results는 분석값을 보고한다.  
Discussion은 결과의 의미, 한계, 향후 연구를 논의한다.

### 시험 포인트

- “숫자가 계산 가능한가?”를 기준으로 categorical/numerical을 구분한다.
- 논문에서 RQ/H는 보통 Introduction 마지막에 나온다.
- Method의 Measures에는 operational definition이 들어간다.

---

## Week 4. 신뢰도, 타당도, 표본추출

### Reliability

신뢰도는 측정의 일관성이다.

예시:

- 같은 사람의 혈압을 반복 측정했을 때 비슷한 값이 나오면 reliable하다.
- 하지만 항상 틀린 값이 나오면 reliable하지만 valid하지는 않다.

종류:

- Test-retest reliability
- Intercoder reliability
- Internal consistency / Cronbach’s alpha

### Validity

타당도는 측정의 정확성이다. 즉, 측정도구가 의도한 개념을 제대로 측정하는가의 문제다.

종류:

- Face validity: 겉보기에 적절한가
- Criterion / predictive validity: 기대 결과를 예측하는가
- Construct validity: 이론적으로 관련된 다른 변수들과 예상대로 관련되는가
- Concurrent validity: 이미 검증된 측정도구와 비슷한 결과를 내는가

### Sampling

비확률표본:

- Convenience sampling: 접근 가능한 사람을 뽑음
- Purposive sampling: 연구 목적에 맞는 사람을 의도적으로 뽑음
- Snowball sampling: 참여자가 다른 참여자를 소개

확률표본:

- Simple random sampling
- Systematic sampling
- Stratified sampling
- Cluster sampling

### 구체 예시

Systematic sampling:

- 모집단 N = 100
- 표본 n = 10
- sampling interval = 100 / 10 = 10
- 무작위 시작점이 2라면 2, 12, 22, 32...를 뽑는다.

### 시험 포인트

- Reliability = consistency
- Validity = accuracy
- Validity가 높으려면 reliability가 필요하지만, reliability만으로 validity가 보장되지는 않는다.
- Generalizability는 표본이 모집단을 얼마나 잘 대표하는가와 관련된다.

---

## Week 5. 내적/외적 타당도 위협과 설문 설계

### Internal Validity

내적 타당도는 연구 내부에서 IV와 DV의 관계를 정확히 검증했는가의 문제다.

주요 위협:

- History: 연구 중 외부 사건이 결과에 영향
- Test sensitization: pretest가 posttest에 영향
- Confounding variable: 통제되지 않은 제3변수
- Instrument decay: 측정도구가 낡거나 변함
- Hawthorne effect: 관찰당한다는 사실 때문에 행동이 바뀜
- Self-selection: 자발적 참여자 특성 때문에 표본이 편향됨
- Maturation: 시간이 지나며 참여자가 자연스럽게 변함
- Attrition: 참여자가 중도 탈락
- Interparticipant bias: 참여자끼리 정보를 공유해 결과에 영향
- Researcher bias: 연구자의 기대가 참여자나 자료해석에 영향

### External Validity

외적 타당도는 연구 결과를 연구 밖 상황이나 모집단에 일반화할 수 있는가의 문제다.

예:

- 광고를 실험실에서 집중해서 보는 상황은 집에서 TV를 보며 딴짓하는 실제 상황과 다르다.

### Survey / Interview

장점:

- 비용이 비교적 낮다.
- 넓은 지역의 사람에게 접근 가능하다.
- 태도, 인식, 사적 생각 같은 주관적 정보를 얻을 수 있다.

단점:

- 인과관계를 확정하기 어렵다.
- 응답자가 부정확하게 답할 수 있다.
- 질문 wording과 순서가 결과에 영향을 줄 수 있다.

### 좋은 설문 문항 원칙

- 명확하게 쓴다.
- 짧게 쓴다.
- 지시문을 완전하게 제공한다.
- 응답자가 현실적으로 기억할 수 있는 것을 묻는다.
- 연구 목적과 관련 있는 문항만 넣는다.
- double-barreled question을 피한다.
- leading / biased wording을 피한다.
- 민감한 질문은 완화된 방식으로 묻는다.

### 시험 포인트

- “12월 성수기 때문에 burnout이 증가했다” → History
- “pretest 때문에 posttest 점수가 오른다” → Test sensitization
- “관찰당해서 손을 더 씻는다” → Hawthorne effect
- “어려운 참가자가 중도탈락했다” → Attrition

---

## Week 6. 실험설계

### 실험의 핵심

실험은 IV가 DV에 미치는 인과효과를 검증하기 위한 방법이다.  
핵심은 manipulation과 control이다.

- Treatment group: IV 처치를 받는 집단
- Control group: 처치를 받지 않는 집단
- Manipulation: 연구자가 IV 수준을 결정하는 것
- Intervening variable: IV-DV 관계에 영향을 줄 수 있는 다른 변수

### 집단 등가성 확보 방법

1. Random assignment
2. Pretest
3. Matching

### 실험설계 유형

High control design:

- Pretest-posttest control group design
- Posttest-only control group design

Moderate control design:

- Pretest-posttest nonequivalent group design
- Interrupted time series design

연구환경:

- Laboratory experiment: 통제 강함, 현실성 약할 수 있음
- Field experiment: 현실성 강함, 통제 약할 수 있음

IV 수:

- Single factor design: IV 1개
- Factorial design: IV 2개 이상
  - 예: 3 x 2 design = IV1 수준 3개, IV2 수준 2개, 총 6개 cell

피험자 배정:

- Between-subjects: 서로 다른 참가자가 각 조건에 배정
- Within-subjects: 같은 참가자가 모든 조건을 경험
- Mixed design: 둘의 조합

### Floor / Ceiling Effect

- Floor effect: 많은 참가자가 최저점에 몰려 더 낮아질 여지가 없음
- Ceiling effect: 많은 참가자가 최고점에 몰려 더 높아질 여지가 없음

### 시험 포인트

- 인과관계를 가장 강하게 주장할 수 있는 방법은 실험이다.
- 그러나 실험은 ecological validity/generalizability가 약해질 수 있다.
- Pretest는 집단 등가성을 확인하지만 test sensitization 위험이 있다.

---

## Week 7-9. 중간 점검과 설문 확정

### Week 7

- 오프라인 수업 없음.
- 조별로 questionnaire를 완성하는 기간.
- CHI conference 자료를 보며 HCI 연구 흐름을 참고하도록 안내.

### Week 8

- Midterm exam.
- 구성: 객관식 20문항 + 단답형 1문항, 60분.

### Week 9

- Questionnaire finalization.
- 각 조는 교수자와 5-10분 미팅을 통해 questionnaire를 수정한다.
- 중간 paper는 점수화보다는 최종 연구 방향 점검 목적이다.

### Midterm / Final Paper 형식

포함해야 할 것:

- 연구 목적
- 연구의 중요성과 기대 함의
- RQ/H
- 가설의 이론적 근거
- IV와 측정 문항
- DV와 측정 문항
- 배경정보 문항
- 내부용 questionnaire appendix

### 시험/과제 포인트

- 설문은 최소 10문항.
- IV/DV 문항 번호를 정확히 연결해야 한다.
- 실제 참가자용 설문에는 “이 문항은 IV입니다” 같은 라벨을 보이면 안 된다.

---

## Week 10. 기술통계

### Descriptive Statistics

기술통계는 표본 데이터를 요약하는 것이다.

대표 항목:

- Frequency
- Percentage
- Mean
- Median
- Mode
- Range
- Standard deviation

### Distribution

- Frequency distribution: 각 값이나 범주의 빈도
- Normal curve: 평균, 중앙값, 최빈값이 같은 대칭 분포
- Skew: 비대칭성
  - Positive skew: 꼬리가 오른쪽
  - Negative skew: 꼬리가 왼쪽
- Kurtosis: 분포의 뾰족함
  - Leptokurtic: 뾰족함
  - Platykurtic: 납작함

### Central Tendency

- Mean: 평균
- Median: 중앙값
- Mode: 최빈값

### Dispersion

- Range: 최댓값 - 최솟값
- Standard deviation: 평균으로부터 점수들이 얼마나 떨어져 있는지

### 보고 기준

- Categorical variable → frequency / percentage
- Numerical variable → mean / standard deviation

### 시험 포인트

- 평균이 같아도 SD가 다르면 데이터의 분산 정도가 다르다.
- 정규분포에서는 ±1 SD 안에 약 68%, ±2 SD 안에 약 95%, ±3 SD 안에 약 99%가 포함된다.
- Outlier는 range에 큰 영향을 준다.

---

## Week 11. 추론통계와 가설검정

### Inferential Statistics

추론통계는 표본에서 얻은 통계량으로 모집단의 모수를 추론하는 것이다.

- Sample statistic: 표본에서 계산한 값
- Population parameter: 모집단의 실제 값

### Hypothesis Testing

- Research hypothesis / Alternative hypothesis:
  - 관계나 차이가 있다고 주장
- Null hypothesis:
  - 관계나 차이가 없다고 주장

검정 논리:

1. 영가설이 맞다고 가정한다.
2. 관찰된 차이/관계가 우연으로 보기 어려울 만큼 큰지 판단한다.
3. 충분히 크면 영가설을 기각한다.

### Statistical Significance

- p < .05:
  - 이 정도 차이가 우연히 나올 확률이 5% 이하
  - 사회과학에서 흔히 쓰는 기준

### Type I / Type II Error

- Type I error:
  - 영가설이 참인데 기각함
  - 실제 효과가 없는데 있다고 결론
  - alpha와 관련

- Type II error:
  - 영가설이 거짓인데 기각하지 못함
  - 실제 효과가 있는데 없다고 결론
  - beta와 관련

- Power:
  - 실제 효과가 있을 때 영가설을 제대로 기각하는 능력
  - 1 - beta

### 시험 포인트

- “reject the null”은 연구가설을 지지하는 방향이다.
- “fail to reject the null”은 연구가설을 지지할 충분한 증거가 없다는 뜻이지, 영가설이 참이라고 증명한 것은 아니다.
- alpha를 낮추면 Type I error는 줄지만 Type II error는 늘 수 있다.

---

## Week 12. 척도 구성과 t-test

### Scale Construction

여러 문항으로 하나의 변수를 만들 때 절차:

1. Reverse coding
   - 부정문항을 방향이 맞게 뒤집는다.
   - 7점 척도라면 1↔7, 2↔6, 3↔5, 4↔4

2. Reliability test
   - Cronbach’s alpha 확인
   - 보통 .80 이상이면 좋다고 판단
   - “Cronbach’s alpha if item deleted”를 보고 문제 문항 제거 가능

3. Compute variable
   - 신뢰도 있는 문항들의 평균으로 새 변수 생성
   - 예: enjoyment = (boringr + enjoyable + not_excitingr) / 3

### T-test

t-test는 두 집단의 평균 차이를 검정한다.

조건:

- IV: categorical, 두 집단
- DV: numerical

유형:

- Independent samples t-test:
  - 서로 다른 두 집단 비교
  - 예: male vs female, treatment vs control

- Paired samples t-test:
  - 같은 사람의 두 시점 비교
  - 예: pretest vs posttest

### 결과 보고 예시 구조

“분석 결과, A 집단과 B 집단의 DV 평균 차이는 유의했다/유의하지 않았다, t(df) = 값, p = 값. A 집단의 평균은 M = 값, SD = 값이고, B 집단의 평균은 M = 값, SD = 값이었다.”

### 시험 포인트

- 두 집단 평균 비교면 t-test.
- 같은 사람 전후 비교면 paired samples t-test.
- 서로 다른 집단이면 independent samples t-test.
- p < .05이면 영가설 기각.

---

## Week 13. Correlation, Chi-square, 최종시험 데이터

### Correlation

상관분석은 두 수치형 변수의 선형관계를 본다.

조건:

- IV: numerical
- DV: numerical

Pearson’s r:

- -1: 완벽한 음의 관계
- 0: 선형관계 없음
- +1: 완벽한 양의 관계

해석:

- r이 양수면 X가 증가할 때 Y도 증가
- r이 음수면 X가 증가할 때 Y는 감소
- 절대값이 클수록 관계가 강함

주의:

- correlation은 선형관계만 잡는다.
- outlier에 민감하다.
- scatter plot을 먼저 확인해야 한다.

### Chi-square

Chi-square는 범주형 변수의 빈도 차이를 검정한다.

조건:

- IV: categorical
- DV: categorical

핵심 논리:

- Observed frequency: 실제 관찰 빈도
- Expected frequency: 영가설이 맞을 때 기대되는 빈도
- 두 값의 차이가 충분히 크면 영가설 기각

df 계산:

`df = (rows - 1) x (columns - 1)`

예:

- 성별과 미소 여부
- 교육수준과 지식 여부

### 분석 선택표

| 연구질문 | IV | DV | 분석 |
|---|---|---|---|
| 두 집단 평균 차이? | categorical, 2 groups | numerical | t-test |
| 두 수치형 변수 관계? | numerical | numerical | correlation |
| 범주별 빈도 차이? | categorical | categorical | chi-square |
| 세 집단 이상 평균 차이? | categorical, 3+ groups | numerical | ANOVA |

### 최종시험 데이터

자료는 VR 관광마케팅 실험 데이터다.

논문/데이터 핵심 구조:

- Design: 2 x 2 between-subjects
- IV1: media type
  - HMD
  - computer
- IV2: information source
  - tour guide
  - peer
- 주요 DV:
  - destination image
  - intention to visit
  - physical presence
  - social presence
  - self-presence

논문 주요 결과:

- HMD는 computer보다 destination image를 더 긍정적으로 만들었다.
- HMD가 intention to visit에 미치는 직접효과는 유의하지 않았다.
- self-presence는 media type과 destination image 사이를 매개했다.
- peer vs tour guide 정보원 차이는 유의하지 않았다.

### 최종시험 연습 흐름

1. Dataset을 SPSS로 연다.
2. Physical presence, social presence, self-presence 문항을 확인한다.
3. 필요한 문항은 reverse coding한다.
4. Cronbach’s alpha로 신뢰도 확인한다.
5. 평균을 내서 새 변수 생성한다.
6. Gender에 따라 presence 평균이 다른지 t-test 한다.
7. 결과를 3-5문장으로 해석한다.

---

## 한 장짜리 시험 대비 요약

### RQ/H 판단

- 물음표가 있으면 RQ
- 문장형 예측이면 H
- 방향을 말하면 directional / one-tailed
- 방향 없이 관계나 차이만 말하면 non-directional / two-tailed

### 변수 판단

- 원인/조건/집단 → IV
- 결과/태도/점수/행동 → DV

### 측정수준 판단

- 이름만 구분 → nominal
- 순서 있음 → ordinal
- 같은 간격, 절대 0 없음 → interval
- 같은 간격, 절대 0 있음 → ratio

### 통계 선택

- categorical + categorical → chi-square
- categorical 2 groups + numerical → t-test
- numerical + numerical → correlation
- categorical 3+ groups + numerical → ANOVA

### 결과 해석

- p < .05 → statistically significant → reject H0
- p >= .05 → not significant → fail to reject H0
- t-test는 평균 차이
- correlation은 관계 방향과 강도
- chi-square는 빈도 차이

### SPSS 절차

- 척도 만들기:
  - reverse coding → reliability analysis → compute mean variable
- descriptive statistics:
  - categorical: frequency
  - numerical: mean, SD
- inferential statistics:
  - t-test / correlation / chi-square 중 변수 유형에 맞게 선택
