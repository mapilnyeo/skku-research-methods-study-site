const weeks = [
  {
    id: 1,
    phase: "design",
    title: "과목 소개와 과학적 앎",
    summary: "전통적 앎과 과학적 앎을 구분하고, 사회과학 연구가 집단 수준의 확률적 패턴을 설명한다.",
    tags: ["science", "logic", "observation", "variable"],
    concepts: [
      "Tenacity, intuition, authority는 과학적 검증 없이 믿음의 근거가 될 수 있다.",
      "과학적 앎은 논리적 설명과 관찰 가능한 자료가 함께 있어야 한다.",
      "Variable은 속성들의 묶음이고 attribute는 변수의 구체적 값이다."
    ],
    examples: [
      "학생증 사진에서 gender와 smiling을 코딩한 뒤 chi-square로 관계를 분석한다.",
      "성별은 male=1, female=2처럼 숫자를 붙여도 수치형이 아니라 범주형이다."
    ],
    exam: [
      "과학적 연구는 단순 믿음이 아니라 logic과 observation에 기반한다.",
      "사회과학은 개인 사례보다 regularity와 probabilistic pattern을 본다."
    ],
    materials: ["Syllabus", "Introducing myself", "Ways of Knowing"]
  },
  {
    id: 2,
    phase: "design",
    title: "연구설계, 인과성, 연구문제와 가설",
    summary: "인과관계의 조건, 연구설계 절차, RQ와 hypothesis를 구분한다.",
    tags: ["causality", "RQ", "hypothesis", "IV/DV"],
    concepts: [
      "인과관계는 correlation, time order, nonspuriousness가 모두 필요하다.",
      "RQ는 질문형이고 hypothesis는 예측 진술문이다.",
      "선행연구로 방향을 예측할 수 있으면 hypothesis, 어렵다면 RQ를 쓴다."
    ],
    examples: [
      "Will Facebook use affect psychological well-being?은 RQ다.",
      "Facebook use will be positively related to psychological well-being.은 directional hypothesis다.",
      "Celebrity endorser advertisement는 IV, brand attitude는 DV다."
    ],
    exam: [
      "increase, decrease, higher, positive 같은 표현은 directional 가능성이 높다.",
      "IV는 원인 또는 예측변수, DV는 결과 또는 영향을 받는 변수다."
    ],
    materials: ["Week2 slides", "Variables worksheet"]
  },
  {
    id: 3,
    phase: "measurement",
    title: "측정수준, APA, 연구논문 구조",
    summary: "추상적 construct를 관찰 가능한 변수로 바꾸고 측정수준을 구분한다.",
    tags: ["measurement", "APA", "nominal", "ratio"],
    concepts: [
      "Nominal은 이름만 구분하고, ordinal은 순서가 있다.",
      "Interval은 동간격이 있지만 절대 0이 없고, ratio는 절대 0이 있다.",
      "논문은 Title, Abstract, Introduction, Method, Results, Discussion, References로 구성된다."
    ],
    examples: [
      "Gender, religion은 nominal이다.",
      "Education level은 ordinal이다.",
      "Age, income, number of hours는 ratio다."
    ],
    exam: [
      "측정수준은 나중에 사용할 통계분석을 결정한다.",
      "Method의 Measures에는 operational definition이 들어간다.",
      "RQ/H는 보통 Introduction 마지막에 배치된다."
    ],
    materials: ["Levels of measurement", "APA guideline", "Research paper structure"]
  },
  {
    id: 4,
    phase: "measurement",
    title: "신뢰도, 타당도, 표본추출",
    summary: "측정의 일관성과 정확성을 구분하고 표본추출 방식을 이해한다.",
    tags: ["reliability", "validity", "sampling"],
    concepts: [
      "Reliability는 측정의 일관성이다.",
      "Validity는 측정도구가 의도한 개념을 정확히 측정하는가의 문제다.",
      "Probability sampling은 random selection을 통해 대표성을 확보하려는 방식이다."
    ],
    examples: [
      "혈압계가 항상 비슷한 값을 내면 reliable하지만, 늘 틀린 값이면 valid하지 않다.",
      "Systematic sampling은 모집단 100명에서 표본 10명을 뽑을 때 10명 간격으로 선택한다."
    ],
    exam: [
      "Reliability = consistency, Validity = accuracy.",
      "Validity가 높으려면 reliability가 필요하지만, reliability만으로 validity가 보장되지는 않는다.",
      "Generalizability는 표본이 모집단을 얼마나 잘 대표하는가와 관련된다."
    ],
    materials: ["Sampling", "Reliability and validity", "Sampling worksheets"]
  },
  {
    id: 5,
    phase: "measurement",
    title: "타당도 위협과 설문 설계",
    summary: "내적/외적 타당도 위협과 좋은 설문 문항의 기준을 배운다.",
    tags: ["internal validity", "external validity", "survey"],
    concepts: [
      "Internal validity는 연구 내부에서 IV-DV 관계를 정확히 검증했는가의 문제다.",
      "External validity는 연구 결과를 연구 밖 상황과 모집단에 일반화할 수 있는가의 문제다.",
      "설문은 명확하고 짧고, 목적과 관련 있으며, 편향된 wording을 피해야 한다."
    ],
    examples: [
      "연구 중 외부 사건이 결과에 영향을 주면 history threat다.",
      "pretest 자체가 posttest 결과를 바꾸면 test sensitization이다.",
      "관찰당한다는 사실 때문에 행동이 바뀌면 Hawthorne effect다."
    ],
    exam: [
      "Double-barreled question은 한 문항에 두 내용을 동시에 묻는 오류다.",
      "Leading question은 응답을 특정 방향으로 유도한다.",
      "Attrition은 참여자가 중도 탈락해 결과가 왜곡되는 상황이다."
    ],
    materials: ["Validity threats", "Survey and interview", "Questionnaire worksheet"]
  },
  {
    id: 6,
    phase: "design",
    title: "실험설계",
    summary: "Manipulation과 control을 중심으로 인과효과를 검증하는 방법을 배운다.",
    tags: ["experiment", "manipulation", "random assignment"],
    concepts: [
      "실험은 IV가 DV에 미치는 인과효과를 검증하는 가장 강한 방법이다.",
      "Treatment group은 처치를 받고, control group은 처치를 받지 않는다.",
      "집단 등가성은 random assignment, pretest, matching으로 확보한다."
    ],
    examples: [
      "3 x 2 factorial design은 IV1 수준 3개와 IV2 수준 2개로 총 6개 cell을 만든다.",
      "Between-subjects는 서로 다른 참가자가 각 조건에 배정되는 설계다.",
      "Within-subjects는 같은 참가자가 모든 조건을 경험하는 설계다."
    ],
    exam: [
      "Pretest는 집단 등가성을 확인하지만 test sensitization 위험이 있다.",
      "Lab experiment는 통제가 강하지만 현실성과 일반화가 약할 수 있다.",
      "Floor/ceiling effect는 점수가 바닥이나 천장에 몰려 효과 탐지가 어려운 상황이다."
    ],
    materials: ["Experimental method", "Experimental design", "Floor and ceiling effect"]
  },
  {
    id: 7,
    phase: "exam",
    title: "중간 점검과 설문지 보완",
    summary: "조별 questionnaire를 완성하고 연구 변수와 문항 연결을 점검한다.",
    tags: ["questionnaire", "project", "CHI"],
    concepts: [
      "조별 연구의 IV/DV가 설문 문항과 정확히 연결되어야 한다.",
      "실제 참가자용 설문에는 IV/DV 같은 내부 분석 라벨을 노출하지 않는다.",
      "CHI 자료는 HCI 연구 질문과 방법을 참고하는 자료로 활용된다."
    ],
    examples: [
      "설문 문항은 최소 10문항을 기준으로 구성한다.",
      "배경정보 문항과 핵심 변수 측정 문항을 구분한다."
    ],
    exam: [
      "설문 문항 번호와 IV/DV 연결을 과제 문서에서 명확히 표시한다.",
      "문항은 응답자가 이해할 수 있는 언어로 작성한다."
    ],
    materials: ["April announcement", "Midterm paper format"]
  },
  {
    id: 8,
    phase: "exam",
    title: "Midterm Exam",
    summary: "연구방법론 앞부분의 핵심 판단을 시험 형식으로 점검한다.",
    tags: ["midterm", "RQ/H", "measurement"],
    concepts: [
      "시험 범위는 연구 질문, 가설, 변수, 측정수준, 신뢰도/타당도, 표본추출을 포함한다.",
      "문항 형태는 객관식 20문항과 단답형 1문항으로 안내되었다."
    ],
    examples: [
      "문장 하나를 보고 RQ인지 hypothesis인지 판단한다.",
      "연구문제에서 IV와 DV를 찾아낸다.",
      "측정 문항의 수준을 nominal, ordinal, interval, ratio로 분류한다."
    ],
    exam: [
      "RQ/H, IV/DV, measurement level은 빠르게 표시할 수 있어야 한다.",
      "타당도 위협 사례와 이름을 연결하는 문제가 나올 수 있다."
    ],
    materials: ["Midterm exam guidance"]
  },
  {
    id: 9,
    phase: "design",
    title: "Questionnaire Finalization",
    summary: "조별 설문지를 최종화하고 분석 가능한 변수 구조로 정리한다.",
    tags: ["questionnaire", "paper", "variables"],
    concepts: [
      "중간 paper는 최종 연구 방향을 점검하기 위한 문서다.",
      "연구 목적, 중요성, RQ/H, IV/DV, 측정 문항이 모두 연결되어야 한다.",
      "설문지는 분석 가능한 형태의 변수로 정리되어야 한다."
    ],
    examples: [
      "IV 문항이 여러 개라면 나중에 scale variable로 묶을 수 있는지 확인한다.",
      "배경정보 문항은 핵심 가설 검정 변수와 구분한다."
    ],
    exam: [
      "연구 목적과 설문 문항이 따로 놀면 설계가 약해진다.",
      "문항은 분석 단계에서 어떤 변수로 쓰일지 미리 생각해야 한다."
    ],
    materials: ["Questionnaire finalization", "SPSS install notice"]
  },
  {
    id: 10,
    phase: "stats",
    title: "기술통계",
    summary: "데이터를 frequency, percentage, mean, SD 같은 요약값으로 이해한다.",
    tags: ["descriptive statistics", "mean", "SD"],
    concepts: [
      "기술통계는 표본 데이터를 이해 가능한 요약값으로 줄이는 방법이다.",
      "Categorical variable은 frequency와 percentage로 보고한다.",
      "Numerical variable은 mean과 standard deviation으로 보고한다."
    ],
    examples: [
      "평균이 같아도 SD가 다르면 점수 분포가 다르다.",
      "Positive skew는 꼬리가 오른쪽으로 긴 분포다.",
      "정규분포에서는 평균, 중앙값, 최빈값이 같다."
    ],
    exam: [
      "±1 SD 안에는 약 68%, ±2 SD 안에는 약 95%가 포함된다.",
      "Outlier는 range에 큰 영향을 준다.",
      "빈도표는 범주별 빈도와 퍼센트를 함께 본다."
    ],
    materials: ["Descriptive statistics", "CSV data", "Excel dataset"]
  },
  {
    id: 11,
    phase: "stats",
    title: "추론통계와 가설검정",
    summary: "표본 통계량으로 모집단을 추론하고 p-value로 유의성을 판단한다.",
    tags: ["inferential statistics", "p-value", "error"],
    concepts: [
      "Sample statistic은 표본에서 계산한 값이고 population parameter는 모집단의 실제 값이다.",
      "검정은 영가설이 맞다고 가정한 뒤 관찰값이 얼마나 이례적인지 판단한다.",
      "p < .05는 우연으로 보기 어려운 결과라는 사회과학의 일반 기준이다."
    ],
    examples: [
      "Type I error는 실제 효과가 없는데 있다고 결론내리는 오류다.",
      "Type II error는 실제 효과가 있는데 없다고 결론내리는 오류다.",
      "Power는 실제 효과가 있을 때 영가설을 제대로 기각하는 능력이다."
    ],
    exam: [
      "Reject the null은 연구가설을 지지하는 방향이다.",
      "Fail to reject the null은 영가설이 참임을 증명한 것이 아니다.",
      "Alpha를 낮추면 Type I error는 줄지만 Type II error는 늘 수 있다."
    ],
    materials: ["Inferential statistics"]
  },
  {
    id: 12,
    phase: "stats",
    title: "척도 구성과 t-test",
    summary: "문항을 척도로 묶고 두 집단 평균 차이를 t-test로 검정한다.",
    tags: ["scale", "Cronbach alpha", "t-test"],
    concepts: [
      "부정문항은 reverse coding으로 방향을 맞춘다.",
      "Cronbach's alpha로 문항들이 같은 개념을 안정적으로 측정하는지 확인한다.",
      "t-test는 IV가 범주형 2집단이고 DV가 수치형일 때 사용한다."
    ],
    examples: [
      "7점 척도 reverse coding은 1↔7, 2↔6, 3↔5, 4↔4로 바꾼다.",
      "서로 다른 male/female 집단 비교는 independent samples t-test다.",
      "같은 사람의 pretest/posttest 비교는 paired samples t-test다."
    ],
    exam: [
      "척도 생성 순서는 reverse coding → reliability analysis → compute mean variable이다.",
      "결과 보고에는 집단별 M, SD, t(df), p가 들어간다.",
      "p < .05이면 평균 차이가 통계적으로 유의하다고 해석한다."
    ],
    materials: ["Scale construction", "T-test", "SPSS worksheets", "CSV datasets"]
  },
  {
    id: 13,
    phase: "stats",
    title: "Correlation, Chi-square, 최종시험 데이터",
    summary: "수치형 관계는 correlation, 범주형 빈도 관계는 chi-square로 분석한다.",
    tags: ["correlation", "chi-square", "final exam"],
    concepts: [
      "Pearson's r은 -1에서 +1 사이이며 부호는 방향, 절대값은 강도를 뜻한다.",
      "Correlation은 선형관계를 보므로 scatter plot과 outlier 확인이 필요하다.",
      "Chi-square는 observed frequency와 expected frequency의 차이를 검정한다."
    ],
    examples: [
      "두 수치형 변수의 관계를 보면 correlation을 사용한다.",
      "성별과 미소 여부처럼 두 범주형 변수는 chi-square를 사용한다.",
      "df는 (rows - 1) x (columns - 1)로 계산한다."
    ],
    exam: [
      "VR 관광 데이터는 2 x 2 between-subjects design이다.",
      "Media type은 HMD vs computer, information source는 tour guide vs peer다.",
      "Self-presence는 media type과 destination image 사이를 매개했다."
    ],
    materials: ["Correlation", "Chi-square", "Final exam dataset", "VR tourism paper"]
  }
];

const phaseLabels = {
  design: "연구설계",
  measurement: "측정/타당도",
  stats: "통계분석",
  exam: "시험대비"
};

const friendlyGuides = {
  1: {
    sentence: "과학적 연구는 느낌이 아니라, 논리와 관찰로 확인하는 과정이다.",
    example: "누군가 “여학생이 남학생보다 더 자주 웃는다”고 말하면 바로 믿지 않는다. 사진을 모으고, 미소 여부를 기준으로 코딩한 뒤, 실제로 차이가 있는지 확인한다.",
    steps: [
      "먼저 주장의 근거가 전통, 직감, 권위인지 구분한다.",
      "그다음 관찰 가능한 자료가 있는지 확인한다.",
      "자료를 숫자나 범주로 정리하면 분석할 수 있다."
    ],
    checks: [
      "“원래 그래”는 과학적 근거가 아니다.",
      "Variable은 큰 범주, attribute는 그 범주의 실제 값이다."
    ]
  },
  2: {
    sentence: "연구문제는 질문이고, 가설은 결과를 미리 예측한 문장이다.",
    example: "“알림을 많이 받으면 집중력이 떨어질까?”는 RQ다. “알림이 많을수록 집중력 점수는 낮아질 것이다”는 방향이 있는 hypothesis다.",
    steps: [
      "문장이 질문형인지 예측형인지 먼저 본다.",
      "원인처럼 보이는 것을 IV로 표시한다.",
      "결과처럼 보이는 것을 DV로 표시한다.",
      "증가, 감소, 높다, 낮다 같은 단어가 있으면 방향성을 의심한다."
    ],
    checks: [
      "인과관계는 관계, 시간순서, 제3변수 배제가 필요하다.",
      "IV는 원인 또는 예측변수, DV는 결과 변수다."
    ]
  },
  3: {
    sentence: "변수가 어떤 숫자인지보다, 그 숫자로 무엇을 할 수 있는지가 중요하다.",
    example: "학년은 1, 2, 3처럼 숫자로 쓰지만 계산용 숫자는 아니다. 순서가 있으므로 ordinal이다. 반대로 하루 공부 시간은 0시간이 가능하므로 ratio다.",
    steps: [
      "이름만 구분하면 nominal로 본다.",
      "순서만 있으면 ordinal로 본다.",
      "간격이 같지만 절대 0이 없으면 interval로 본다.",
      "간격이 같고 절대 0이 있으면 ratio로 본다."
    ],
    checks: [
      "Nominal과 ordinal은 보통 categorical로 묶는다.",
      "Interval과 ratio는 보통 numerical로 묶는다."
    ]
  },
  4: {
    sentence: "신뢰도는 일관성, 타당도는 정확성이다.",
    example: "체중계가 매번 실제보다 3kg 무겁게 나온다면 일관성은 있다. 하지만 정확하지 않다. 그래서 reliable할 수는 있지만 valid하지 않다.",
    steps: [
      "같은 결과가 반복되는지 보면 reliability다.",
      "정말 재려던 것을 재고 있는지 보면 validity다.",
      "표본이 모집단을 대표하는지 보면 generalizability다."
    ],
    checks: [
      "타당하려면 어느 정도 신뢰도가 필요하다.",
      "하지만 신뢰도가 높다고 항상 타당한 것은 아니다."
    ]
  },
  5: {
    sentence: "좋은 설문은 응답자가 고민 없이 이해하고 답할 수 있어야 한다.",
    example: "“이 앱은 편리하고 예쁜가요?”는 좋지 않다. 편리함과 예쁨을 한 문항에 같이 묻기 때문이다. “이 앱은 사용하기 편리하다”와 “이 앱은 디자인이 보기 좋다”로 나누는 것이 좋다.",
    steps: [
      "한 문항에는 하나만 묻는다.",
      "응답자가 기억하기 어려운 질문은 피한다.",
      "특정 답을 유도하는 표현을 빼고 중립적으로 쓴다.",
      "민감한 질문은 완화된 표현으로 묻는다."
    ],
    checks: [
      "Double-barreled question은 두 내용을 한 번에 묻는다.",
      "Leading question은 응답을 특정 방향으로 끌고 간다."
    ]
  },
  6: {
    sentence: "실험은 원인을 직접 조작해서 결과가 달라지는지 보는 방법이다.",
    example: "수면 앱을 쓰는 집단과 쓰지 않는 집단을 나누고 수면시간을 비교한다. 여기서 앱 사용 여부가 IV, 수면시간이 DV다.",
    steps: [
      "먼저 연구자가 바꾸는 조건을 찾는다.",
      "그 조건을 받은 집단과 받지 않은 집단을 구분한다.",
      "두 집단이 처음부터 비슷하도록 random assignment를 사용한다.",
      "결과 변수에서 차이가 나는지 확인한다."
    ],
    checks: [
      "실험은 인과관계를 가장 강하게 말할 수 있다.",
      "하지만 너무 통제된 실험은 현실 적용이 약할 수 있다."
    ]
  },
  7: {
    sentence: "설문지는 연구자용 구조와 참가자용 문장을 분리해서 봐야 한다.",
    example: "연구자는 어떤 문항이 IV인지 DV인지 알아야 한다. 하지만 참가자에게는 그런 라벨을 보여주지 않고 자연스러운 설문 문장만 보여준다.",
    steps: [
      "연구 목적을 한 문장으로 적는다.",
      "IV 문항과 DV 문항을 따로 표시한다.",
      "참가자에게 보일 실제 설문에서는 분석용 표시를 제거한다."
    ],
    checks: [
      "문항 번호와 변수 연결을 과제 문서에서 분명히 표시한다.",
      "참가자용 설문은 자연스럽고 짧아야 한다."
    ]
  },
  8: {
    sentence: "시험 문제는 먼저 표시하고 나서 풀면 부담이 줄어든다.",
    example: "문장을 받으면 물음표인지, 예측 문장인지, 원인이 무엇인지, 결과가 무엇인지 순서대로 표시한다. 그러면 RQ/H와 IV/DV가 같이 정리된다.",
    steps: [
      "물음표가 있는지 본다.",
      "예측 방향 표현이 있는지 본다.",
      "원인처럼 보이는 단어에 IV를 표시한다.",
      "결과처럼 보이는 단어에 DV를 표시한다."
    ],
    checks: [
      "RQ/H, IV/DV, measurement level을 빠르게 표시한다.",
      "타당도 위협은 사례와 이름을 연결해서 외운다."
    ]
  },
  9: {
    sentence: "좋은 설문지는 나중에 SPSS에서 바로 분석할 수 있게 만들어져야 한다.",
    example: "만족도 문항이 여러 개라면 나중에 평균을 내서 하나의 만족도 점수로 만들 수 있다. 그래서 문항 방향과 응답 척도를 미리 맞춰두는 것이 중요하다.",
    steps: [
      "각 문항이 어떤 변수에 속하는지 적는다.",
      "응답 척도가 서로 같은지 확인한다.",
      "부정문항이 있으면 나중에 reverse coding할 수 있게 표시한다.",
      "배경정보 문항과 핵심 변수 문항을 분리한다."
    ],
    checks: [
      "연구 목적과 설문 문항이 연결되어야 한다.",
      "분석할 수 없는 문항은 좋은 연구문항이 아니다."
    ]
  },
  10: {
    sentence: "기술통계는 복잡한 데이터를 한눈에 보이게 줄이는 요약이다.",
    example: "두 반의 평균 점수가 80점으로 같아도, 한 반은 모두 78-82점이고 다른 반은 50점부터 100점까지 흩어질 수 있다. 이 차이를 standard deviation이 보여준다.",
    steps: [
      "범주형 변수는 빈도와 퍼센트를 본다.",
      "수치형 변수는 평균과 표준편차를 본다.",
      "분포가 치우쳤는지 skew를 확인한다.",
      "극단값이 있으면 평균과 range 해석을 조심한다."
    ],
    checks: [
      "Mean은 중심, SD는 흩어짐이다.",
      "Categorical은 frequency, numerical은 mean과 SD가 기본이다."
    ]
  },
  11: {
    sentence: "추론통계는 표본에서 본 결과가 모집단에서도 그럴지 판단하는 과정이다.",
    example: "우리 반 30명만 조사했는데 전체 학생에게도 비슷한 경향이 있을까? 이 질문을 확률적으로 판단하는 것이 추론통계다.",
    steps: [
      "영가설은 차이나 관계가 없다고 가정한다.",
      "관찰된 결과가 우연으로 보기 어려운지 본다.",
      "p-value가 기준보다 작으면 영가설을 기각한다.",
      "기각하지 못했다고 해서 영가설이 참으로 증명된 것은 아니다."
    ],
    checks: [
      "p < .05는 사회과학에서 흔히 쓰는 기준이다.",
      "Type I error는 없는데 있다고 판단하는 오류다."
    ]
  },
  12: {
    sentence: "t-test는 두 평균이 정말 다른지 확인하는 분석이다.",
    example: "남학생과 여학생의 평균 만족도를 비교하면 independent t-test다. 같은 학생의 수업 전 만족도와 수업 후 만족도를 비교하면 paired t-test다.",
    steps: [
      "DV가 수치형인지 확인한다.",
      "IV가 두 집단인지 확인한다.",
      "서로 다른 사람끼리 비교하면 independent t-test다.",
      "같은 사람을 두 번 잰 것이면 paired t-test다."
    ],
    checks: [
      "척도 생성은 reverse coding, reliability analysis, compute mean 순서다.",
      "결과 보고에는 M, SD, t(df), p가 들어간다."
    ]
  },
  13: {
    sentence: "두 변수가 모두 숫자면 correlation, 둘 다 범주면 chi-square를 먼저 떠올린다.",
    example: "공부 시간과 시험 점수는 둘 다 숫자라서 correlation이다. 성별과 합격 여부는 둘 다 범주라서 chi-square다.",
    steps: [
      "두 변수가 수치형인지 범주형인지 먼저 표시한다.",
      "수치형과 수치형이면 Pearson correlation을 고려한다.",
      "범주형과 범주형이면 chi-square를 고려한다.",
      "VR 데이터는 media type과 information source가 주요 IV라는 점을 기억한다."
    ],
    checks: [
      "Correlation은 관계의 방향과 강도를 본다.",
      "Chi-square는 observed frequency와 expected frequency의 차이를 본다."
    ]
  }
};

const contentView = document.querySelector("#contentView");
const weekNav = document.querySelector("#weekNav");
const progressFill = document.querySelector("#progressFill");
const progressText = document.querySelector("#progressText");
const progressPercent = document.querySelector("#progressPercent");

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function listItems(items) {
  return items.map((item) => `<li>${escapeHtml(item)}</li>`).join("");
}

function getCompletedWeeks() {
  try {
    return JSON.parse(localStorage.getItem("rm_completed_weeks") || "[]");
  } catch {
    return [];
  }
}

function setCompletedWeeks(ids) {
  try {
    localStorage.setItem("rm_completed_weeks", JSON.stringify(ids));
  } catch {
    // file:// 환경에서 저장소 접근이 제한되어도 화면 동작은 유지한다.
  }
}

function updateProgress() {
  const completed = getCompletedWeeks();
  const count = completed.length;
  const percent = Math.round((count / weeks.length) * 100);
  progressText.textContent = `${count} / ${weeks.length} 완료`;
  progressPercent.textContent = `${percent}%`;
  progressFill.style.width = `${percent}%`;
}

function renderNav() {
  weekNav.innerHTML = weeks
    .map((week) => {
      return `
        <a href="#week-${week.id}" data-route="week-${week.id}">
          <span>Week ${week.id}</span>
          <small>${phaseLabels[week.phase]}</small>
        </a>
      `;
    })
    .join("");
}

function getRoute() {
  const route = window.location.hash.replace("#", "") || "overview";
  if (route === "overview" || route === "analysis" || route === "exam") return route;

  const weekMatch = route.match(/^week-(\d+)$/);
  if (weekMatch) {
    const weekId = Number(weekMatch[1]);
    if (weeks.some((week) => week.id === weekId)) return route;
  }

  return "overview";
}

function setActiveNav(route) {
  document.querySelectorAll("[data-route]").forEach((item) => {
    item.classList.toggle("active", item.dataset.route === route);
  });
}

function renderOverview() {
  contentView.innerHTML = `
    <div class="page-shell">
      <section class="page-hero">
        <p class="eyebrow">Start Here</p>
        <h1>한 번에 하나씩 보는 연구방법론 학습 사이트</h1>
        <p class="lead">이제 모든 주차를 한 페이지에 쌓지 않습니다. 왼쪽 메뉴에서 필요한 화면만 열고, 먼저 쉬운 예시를 본 다음 자세한 개념으로 넘어가세요.</p>
        <div class="hero-actions">
          <a class="button-link primary" href="#week-1">Week 1부터 시작</a>
          <a class="button-link" href="#analysis">분석 선택기 열기</a>
        </div>
      </section>

      <section class="panel">
        <p class="eyebrow">Three Questions</p>
        <h2>처음 보면 이 세 질문만 잡기</h2>
        <div class="focus-grid">
          <article class="mini-card">
            <strong>1. 무엇을 알고 싶은가?</strong>
            <p>연구문제 RQ 또는 가설 hypothesis로 바꾼다.</p>
          </article>
          <article class="mini-card">
            <strong>2. 무엇이 원인과 결과인가?</strong>
            <p>원인처럼 보이는 것은 IV, 결과처럼 보이는 것은 DV다.</p>
          </article>
          <article class="mini-card">
            <strong>3. 변수 유형은 무엇인가?</strong>
            <p>범주형인지 수치형인지에 따라 분석법이 달라진다.</p>
          </article>
        </div>
      </section>

      <section class="panel">
        <p class="eyebrow">Easy Examples</p>
        <h2>초보자용 쉬운 예시</h2>
        <div class="guide-grid">
          <article class="mini-card">
            <strong>카페 음악이 머무는 시간에 영향을 줄까?</strong>
            <p>음악 유무가 IV, 카페에 머문 시간이 DV다.</p>
          </article>
          <article class="mini-card">
            <strong>학년은 숫자지만 계산용 숫자는 아니다</strong>
            <p>1학년, 2학년, 3학년은 순서가 있으므로 ordinal이다.</p>
          </article>
          <article class="mini-card">
            <strong>남녀 평균 비교는 t-test</strong>
            <p>성별은 두 집단 범주형 IV이고 만족도는 수치형 DV다.</p>
          </article>
        </div>
      </section>

      <section class="panel">
        <p class="eyebrow">Learning Sequence</p>
        <h2>한 학기 흐름</h2>
        <div class="roadmap-grid">
          ${["질문", "변수", "측정", "표본", "검증", "자료", "분석"]
            .map((step, index) => `<article class="roadmap-step"><strong>${index + 1}. ${step}</strong><p>${[
              "RQ/H로 정리",
              "IV/DV 분리",
              "문항과 측정수준",
              "대상과 표본",
              "신뢰도와 타당도",
              "설문과 실험",
              "통계 선택"
            ][index]}</p></article>`)
            .join("")}
        </div>
      </section>
    </div>
  `;
}

function renderAnalysis() {
  contentView.innerHTML = `
    <div class="page-shell">
      <section class="page-hero">
        <p class="eyebrow">Analysis Picker</p>
        <h1>변수 유형만 알면 분석법이 좁혀진다</h1>
        <p class="lead">분석을 고를 때는 어려운 이름부터 외우지 말고, IV와 DV가 범주형인지 수치형인지 먼저 표시하세요.</p>
      </section>

      <section class="analysis-panel">
        <h2>분석 선택기</h2>
        <div class="choice-grid">
          <label>
            IV 유형
            <select id="ivSelect">
              <option value="cat2">범주형, 2집단</option>
              <option value="cat3">범주형, 3집단 이상</option>
              <option value="cat">범주형</option>
              <option value="num">수치형</option>
              <option value="paired">같은 사람의 전후 측정</option>
            </select>
          </label>
          <label>
            DV 유형
            <select id="dvSelect">
              <option value="num">수치형</option>
              <option value="cat">범주형</option>
            </select>
          </label>
          <div class="analysis-result" id="analysisResult" aria-live="polite"></div>
        </div>
      </section>

      <section class="panel">
        <p class="eyebrow">Quick Rules</p>
        <h2>헷갈릴 때 보는 기준</h2>
        <div class="concept-grid">
          <article class="concept-card"><strong>t-test</strong><p>두 집단 평균 비교. IV는 범주형 2집단, DV는 수치형.</p></article>
          <article class="concept-card"><strong>Correlation</strong><p>두 수치형 변수의 관계. r의 부호는 방향, 절대값은 강도.</p></article>
          <article class="concept-card"><strong>Chi-square</strong><p>두 범주형 변수의 빈도 차이. observed와 expected를 비교.</p></article>
          <article class="concept-card"><strong>ANOVA</strong><p>세 집단 이상 평균 비교. 이 수업에서는 선택 기준만 알아두면 충분하다.</p></article>
        </div>
      </section>
    </div>
  `;

  bindAnalysisPicker();
}

function renderExam() {
  contentView.innerHTML = `
    <div class="page-shell">
      <section class="page-hero">
        <p class="eyebrow">Exam Kit</p>
        <h1>시험 직전에는 판단 순서를 줄이면 된다</h1>
        <p class="lead">모든 개념을 한꺼번에 떠올리려 하지 말고, 문제를 보면 아래 순서대로 표시하세요.</p>
      </section>

      <section class="exam-panel">
        <h2>시험 풀이 순서</h2>
        <div class="exam-grid">
          <article class="exam-card"><strong>1. RQ/H</strong><p>물음표면 RQ, 예측 진술문이면 hypothesis다.</p></article>
          <article class="exam-card"><strong>2. IV/DV</strong><p>원인, 조건, 집단은 IV. 결과, 태도, 점수는 DV.</p></article>
          <article class="exam-card"><strong>3. 측정수준</strong><p>이름, 순서, 동간격, 절대 0 순서로 본다.</p></article>
          <article class="exam-card"><strong>4. 분석 선택</strong><p>범주+범주 chi-square, 수치+수치 correlation.</p></article>
          <article class="exam-card"><strong>5. t-test</strong><p>두 집단 평균 비교면 t-test를 먼저 떠올린다.</p></article>
          <article class="exam-card"><strong>6. p-value</strong><p>p &lt; .05면 영가설을 기각한다.</p></article>
        </div>
      </section>
    </div>
  `;
}

function renderWeek(route) {
  const weekId = Number(route.replace("week-", ""));
  const week = weeks.find((item) => item.id === weekId);
  const guide = friendlyGuides[weekId];
  const completed = new Set(getCompletedWeeks());
  const checked = completed.has(weekId) ? "checked" : "";
  const prevHref = weekId > 1 ? `#week-${weekId - 1}` : "#overview";
  const nextHref = weekId < weeks.length ? `#week-${weekId + 1}` : "#exam";
  const prevLabel = weekId > 1 ? `이전 Week ${weekId - 1}` : "전체 개요";
  const nextLabel = weekId < weeks.length ? `다음 Week ${weekId + 1}` : "시험 대비";

  contentView.innerHTML = `
    <div class="page-shell">
      <article class="lesson-hero">
        <div class="lesson-topline">
          <span class="badge">Week ${week.id}</span>
          <span class="badge">${phaseLabels[week.phase]}</span>
          <label class="complete-control">
            <input id="weekComplete" type="checkbox" data-week="${week.id}" ${checked} />
            이 주차 완료
          </label>
        </div>
        <h1>${escapeHtml(week.title)}</h1>
        <p class="lead">${escapeHtml(week.summary)}</p>
      </article>

      <div class="lesson-layout">
        <div class="page-shell">
          <section class="big-note">
            <span>오늘의 한 문장</span>
            <p>${escapeHtml(guide.sentence)}</p>
          </section>

          <section class="easy-example">
            <span>쉬운 예시</span>
            <p>${escapeHtml(guide.example)}</p>
          </section>

          <section class="study-steps">
            <h2>천천히 이해하기</h2>
            <ol>${listItems(guide.steps)}</ol>
          </section>

          <details class="detail-panel">
            <summary>강의 핵심 개념 펼치기</summary>
            <ul>${listItems(week.concepts)}</ul>
          </details>

          <details class="detail-panel">
            <summary>강의 예시 펼치기</summary>
            <ul>${listItems(week.examples)}</ul>
          </details>
        </div>

        <aside class="side-stack" aria-label="보조 학습 정보">
          <section class="memory-box">
            <span>꼭 기억</span>
            <p>${escapeHtml(week.exam[0])}</p>
          </section>

          <section class="detail-panel">
            <h2>헷갈리면 이렇게 판단</h2>
            <ul>${listItems(guide.checks)}</ul>
          </section>

          <section class="detail-panel">
            <h2>태그</h2>
            <div class="tag-row">${week.tags.map((tag) => `<span class="tag">${escapeHtml(tag)}</span>`).join("")}</div>
          </section>

          <section class="detail-panel">
            <h2>관련 자료</h2>
            <div class="materials">${week.materials.map((item) => `<span class="material-pill">${escapeHtml(item)}</span>`).join("")}</div>
          </section>
        </aside>
      </div>

      <nav class="lesson-nav" aria-label="주차 이동">
        <a href="${prevHref}">${prevLabel}</a>
        <a href="${nextHref}">${nextLabel}</a>
      </nav>
    </div>
  `;

  bindCompletion();
}

function bindCompletion() {
  const checkbox = document.querySelector("#weekComplete");
  if (!checkbox) return;

  checkbox.addEventListener("change", () => {
    const weekId = Number(checkbox.dataset.week);
    const completed = new Set(getCompletedWeeks());
    if (checkbox.checked) {
      completed.add(weekId);
    } else {
      completed.delete(weekId);
    }
    setCompletedWeeks([...completed].sort((a, b) => a - b));
    updateProgress();
  });
}

function getAnalysisRule(iv, dv) {
  if (iv === "paired" && dv === "num") {
    return {
      title: "Paired samples t-test",
      body: "같은 사람의 전후 평균 차이를 검정한다.",
      example: "예: 같은 학생의 수업 전 만족도와 수업 후 만족도 비교"
    };
  }
  if (iv === "cat2" && dv === "num") {
    return {
      title: "Independent samples t-test",
      body: "서로 다른 두 집단의 평균 차이를 검정한다.",
      example: "예: 남성과 여성의 presence 평균 비교"
    };
  }
  if (iv === "cat3" && dv === "num") {
    return {
      title: "ANOVA",
      body: "세 집단 이상 평균 차이를 검정한다.",
      example: "예: 1학년, 2학년, 3학년의 평균 만족도 비교"
    };
  }
  if ((iv === "cat" || iv === "cat2" || iv === "cat3") && dv === "cat") {
    return {
      title: "Chi-square",
      body: "두 범주형 변수의 빈도 차이를 검정한다.",
      example: "예: 성별과 합격 여부의 관계 비교"
    };
  }
  if (iv === "num" && dv === "num") {
    return {
      title: "Correlation",
      body: "두 수치형 변수의 선형관계를 검정한다.",
      example: "예: 공부 시간과 시험 점수의 관계"
    };
  }
  return {
    title: "변수 유형 재확인",
    body: "분석 선택 전에 IV/DV의 측정수준과 집단 수를 다시 확인해야 한다.",
    example: "먼저 IV가 범주형인지 수치형인지, DV가 점수인지 범주인지 표시한다."
  };
}

function updateAnalysis() {
  const ivSelect = document.querySelector("#ivSelect");
  const dvSelect = document.querySelector("#dvSelect");
  const result = document.querySelector("#analysisResult");
  if (!ivSelect || !dvSelect || !result) return;

  const rule = getAnalysisRule(ivSelect.value, dvSelect.value);
  result.innerHTML = `
    <strong>${escapeHtml(rule.title)}</strong>
    <span>${escapeHtml(rule.body)}</span>
    <em>${escapeHtml(rule.example)}</em>
  `;
}

function bindAnalysisPicker() {
  const ivSelect = document.querySelector("#ivSelect");
  const dvSelect = document.querySelector("#dvSelect");
  if (!ivSelect || !dvSelect) return;

  ivSelect.addEventListener("change", updateAnalysis);
  dvSelect.addEventListener("change", updateAnalysis);
  updateAnalysis();
}

function renderRoute() {
  const route = getRoute();

  if (route === "overview") renderOverview();
  else if (route === "analysis") renderAnalysis();
  else if (route === "exam") renderExam();
  else renderWeek(route);

  setActiveNav(route);
  updateProgress();
  contentView.focus({ preventScroll: true });
}

renderNav();
renderRoute();

window.addEventListener("hashchange", renderRoute);
