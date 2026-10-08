---
title: Research
ref: research
nav:
  order: 2
  tooltip: 연구분야
---

# {% include icon.html icon="fa-solid fa-rocket" %}Research
{: .page-title }

SEARCH Lab은 우주비행역학과 동역학계 이론을 바탕으로 지구궤도부터 심우주 탐사까지 아우르는 **우주임무 아키텍처**를 설계합니다. 궤도·궤적 해석, 유도·자세 제어, 수치최적화, AI·기계학습과 시스템 분석을 결합해 임무의 실현 가능성을 평가하고 우주실증 방안을 연구합니다.
{: .page-intro }

<nav class="research-nav" aria-label="연구분야 바로가기">
  <a href="#methods">핵심 이론과 방법론</a>
  <a href="#earth-orbit">지구궤도 임무설계</a>
  <a href="#planetary">달·행성 탐사</a>
  <a href="#entry-systems">진입·착륙·열보호</a>
  <a href="#solar-sail">태양돛</a>
  <a href="#optical-communications">심우주 광통신</a>
  <a href="#cubesat">큐브샛·우주실증</a>
</nav>

{% include section.html %}

## 핵심 이론과 방법론 {#methods}

<div class="research-methods" markdown="1">

{% for method in site.data.research-topics.methods %}
<div class="research-method" markdown="1">

{% for alias in method.aliases %}<div id="{{ alias }}" aria-hidden="true"></div>{% endfor %}

<div class="research-method-number" aria-hidden="true">0{{ forloop.index }}</div>

### {{ method.ko.title }} {#{{ method.id }}}

{{ method.ko.summary }}

</div>
{% endfor %}

</div>

{% include research-figure.html topic="architecture" caption="임무 목표와 제약조건을 바탕으로 궤도·궤적·시스템·통신 운용을 연계해 분석·최적화하고, 실현 가능성을 평가해 설계를 다듬습니다." alt="임무 목표와 제약조건에서 출발해 궤도·궤적·기동, 위성·탐사선·탑재체, 통신·운용의 연계 모델을 구성하고, 성능·실현 가능성·민감도·위험 평가를 설계에 반영하는 개념도." %}

{% include section.html %}

## 적용 연구분야 {#applications}

핵심 이론과 방법론을 다음 여섯 분야에 적용하며, 각 분야의 임무 환경과 기술 요구조건에 맞는 문제를 다룹니다.

### {% include icon.html icon="fa-solid fa-globe" %}{% include research-title.html id="earth-orbit" %} {#earth-orbit}

지구관측·통신·기술실증을 위한 지구궤도 임무를 설계합니다. 임무 요구조건에 맞는 궤도와 운용 시나리오를 검토하고, 관측 범위·재방문 주기·지상국 가시성을 분석합니다.

- 지구관측·통신·기술실증 위성의 궤도 고도·경사각과 운용개념 설계
- 관심 지역의 관측 범위·재방문 주기 및 지상국과의 통신 가능 시간 분석
- 지구 비구면 중력·대기저항을 고려한 장기 궤도전파와 궤도유지 전략

#### 군집위성 궤도설계 {#earth-constellation}

여러 위성이 함께 임무를 수행하는 군집위성에서는 위성 수, 궤도면 구성, 위성 간 위상 배치를 함께 설계합니다. 관측·통신 성능과 추진제 소모, 운용 부담의 상충관계를 분석해 배치를 최적화하고, 궤도섭동과 궤도유지 기동을 반영해 장기 임무 성능을 평가합니다.

위성 간 상대 위치를 정밀하게 유지해야 하는 편대비행에서는 상대궤도 동역학과 항법 오차를 고려한 [유도·제어](#guidance-control) 문제로 확장합니다.

{% include research-figure.html topic="earth-constellation" caption="세 궤도면에 위성을 나누어 배치한 군집위성 개념도. 색상은 서로 다른 궤도면을 구분합니다. 설명을 위한 예시로, 크기와 거리는 축척을 따르지 않습니다." alt="지구를 둘러싼 세 원궤도에 여러 위성을 배치하고, 궤도 고도·경사각·궤도면·위성 간 위상을 설계변수로 표시한 개념도." %}

{% include section.html %}

### {% include icon.html icon="fa-solid fa-moon" %}{% include research-title.html id="planetary" %} {#planetary}

달 착륙선과 화성 궤도선·착륙선 등 달·행성 탐사 임무를 설계합니다. 탐사 목표에 맞는 궤도와 착륙지를 검토하고, 탐사선·관측 대상·지구의 상대적 위치가 관측과 통신에 미치는 영향을 분석해 운용 시나리오를 수립합니다.

- 달 탐사·착륙 및 화성 궤도선·착륙선 임무 개념설계
- 탐사 목표에 따른 궤도와 착륙지 검토
- 탐사선·표면 관측 대상·지구 사이의 관측·통신 기하 분석
- 관측·통신 가능 시간을 고려한 탐사선 운용 시나리오 설계

{% include research-figure.html topic="planetary" caption="궤도선·표면 관측 대상·지구의 상대적 위치는 관측 가능 시간과 통신 경로를 결정하는 주요 조건입니다. 크기와 거리는 축척을 따르지 않습니다." alt="천체 주위를 도는 궤도선과 표면 관측 대상, 지구 사이의 관측 방향과 통신 경로를 나타낸 개념도." %}

{% include section.html %}

### {% include icon.html icon="fa-solid fa-parachute-box" %}{% include research-title.html id="entry-systems" %} {#entry-systems}

#### 행성 진입·하강·착륙 {#edl}

화성처럼 대기가 있는 행성에서 탐사선이 대기권에 진입한 뒤 감속하고 안전하게 착륙하는 과정을 연구합니다. 대기와 열공력 환경, 낙하산 전개 조건, 유도·제어 방식이 궤적과 착륙 위치의 오차에 미치는 영향을 분석합니다.

- 화성 대기권 진입경로와 진입 유도 해석
- 낙하산 전개 조건 및 감속·착륙 시나리오 설계
- 대기·열공력 모델을 반영한 3자유도·6자유도 시뮬레이션
- 착륙분산 분석과 행성 착륙 임무 성능 평가

{% include research-figure.html topic="edl" caption="화성 탐사선의 대표적인 진입·하강·착륙 단계. 대기권 진입, 낙하산 감속, 최종 하강과 착륙을 이어 설계하며, 구체적인 방식은 임무에 따라 달라집니다." alt="화성 대기권 진입부터 낙하산을 이용한 감속, 최종 하강, 표면 착륙까지 이어지는 단계별 개념도." %}

#### 지구 재진입과 열보호시스템 {#reentry}

지구로 귀환하는 우주선과 시료귀환 캡슐이 고속으로 대기권에 진입할 때의 공력가열과 감속하중을 분석합니다. 재진입 궤적과 열환경을 함께 고려해 열차폐체 등 열보호시스템을 설계하고 검증하는 방법을 연구합니다.

- 재진입 궤적·진입 회랑 및 시료귀환 캡슐 회수 시나리오 설계
- 공력가열과 감속하중 등 재진입 환경 예측
- 열보호시스템 개념설계·두께 산정 및 삭마형·재사용형 열보호재의 열응답 해석
- 아크제트 등 지상시험과 비행시험을 활용한 검증 방법 연구

{% include research-figure.html topic="reentry" caption="삭마형 열차폐체를 사용하는 귀환 캡슐의 단면 개념도. 열차폐체와 단열층은 내부로 전달되는 열을 줄이며, 실제 층 구성과 두께는 재료와 임무 조건에 따라 달라집니다." alt="극초음속 유동을 마주하는 귀환 캡슐의 충격파와 고온 기체층, 삭마형 열차폐체, 단열층, 내부 탑재체를 구분한 단면 개념도." %}

{% include section.html %}

### {% include icon.html icon="fa-solid fa-sun" %}{% include research-title.html id="solar-sail" %} {#solar-sail}

태양돛은 햇빛이 돛에 운동량을 전달할 때 생기는 태양복사압을 이용해 추력을 얻습니다. 돛의 방향을 조절해 궤적을 바꾸는 원리를 바탕으로, 추진제 사용을 줄이는 장기 비행과 미래 심우주 탐사 임무를 설계합니다.

- 태양복사압과 돛 자세를 고려한 우주비행역학
- 태양돛 기반 궤도상승과 장기 저추력 궤적 설계
- 비케플러 궤도 등 특수궤도와 미래 탐사 임무 개념설계
- 태양돛 우주실증 임무 기획

{% include research-figure.html topic="solar-sail" caption="태양광이 돛에 운동량을 전달해 추력을 만드는 원리. 오른쪽은 이상적인 완전 반사 돛의 단면으로, 돛의 방향에 따라 추력의 크기와 방향이 달라집니다." alt="펼쳐진 태양돛의 전체 형상과 이상적인 반사 돛의 단면. 입사광·반사광과 돛 표면에 수직으로 작용하는 추력을 나타낸 개념도." %}

#### 자세·궤도 통합 제어 {#integrated-attitude-orbit-control}

[유도·제어](#optimization)와 [자세 역학·자세 제어](#attitude-dynamics-control)를 결합해 태양돛의 궤도·자세 운동을 함께 해석하고 제어하는 방법을 연구하고자 합니다. 태양복사압에 의한 힘·토크와 질량중심·압력중심의 관계를 모델링하고, 구동기 한계와 관측·통신 지향 조건을 반영한 6자유도 시뮬레이션으로 임무 수행 가능성을 평가합니다. [AI·기계학습](#ai-machine-learning)을 활용한 제어 명령 예측과 자율비행의 적용 가능성도 검토합니다.

관련 선행연구: [딥러닝 기반 태양돛 최적제어의 간접법 해석 (2025)](https://www.dbpia.co.kr/journal/articleDetail?nodeId=NODE12589746)

#### 태양돛 전개장치 개발 및 지상시험 {#solar-sail-ground-test}

한국항공우주연구원(KARI)은 심우주 탐사에 활용할 태양돛 전개기술을 확보하기 위해 10 m × 10 m(100 m²) 규모의 지상 시험모델을 개발했습니다. 모터로 네 개의 지지대(붐)를 펼치면서 수납된 얇은 돛을 전개하는 구조로, 지상시험을 통해 붐과 돛의 전개 과정에서 발생하는 문제와 개선점을 확인했습니다. 아래 영상은 시험모델의 전개 과정을 상부와 측면에서 촬영한 것입니다.

관련 자료: [항우연 보도자료](https://www.kari.re.kr/kor/article/ATCL87374b48c/18228) · [태양돛 전개 시험 및 교훈](https://doi.org/10.52912/jsta.2026.6.3.293)

<div class="research-video-grid">
{% include research-video.html id="sail-test-overhead" file="kari-solar-sail-deployment-overhead.mp4" poster="kari-solar-sail-deployment-overhead.jpg" title="태양돛 전개시험 · 상부 촬영 (영상 23초)" %}
{% include research-video.html id="sail-test-side" file="kari-solar-sail-deployment-side.mp4" poster="kari-solar-sail-deployment-side.jpg" title="태양돛 전개시험 · 측면 촬영 (영상 22초)" %}
</div>

#### 우주쓰레기 제거용 궤도이탈 장치 개발 및 지상시험 {#deorbiter-ground-test}

한국항공우주연구원(KARI)은 저궤도 우주쓰레기의 포획·제거 기술을 검증하기 위해 궤도이탈 장치(deorbiter)의 지상 시험모델을 개발했습니다. 견인부·포획부·전개부로 구성되며, 5 m × 5 m(25 m²)의 저항돛(drag sail)을 펼쳐 대기저항을 높이고 포획한 물체의 대기권 재진입을 유도하는 개념입니다. 아래 영상은 이 가운데 저항돛의 전개 기능을 확인하는 지상시험 장면입니다.

관련 자료: [항우연 보도자료](https://www.kari.re.kr/kor/article/ATCL87374b48c/18417) · [궤도이탈 장치 개발·시험 논문](https://doi.org/10.52912/jsta.2026.6.2.196)

<div class="research-video-grid">
{% include research-video.html id="deorbiter-test-wide" file="kari-deorbiter-drag-sail-wide.mp4" poster="kari-deorbiter-drag-sail-wide.jpg" title="저항돛 전개시험 · 전체 모습 (영상 2.4초)" %}
{% include research-video.html id="deorbiter-test-overhead" file="kari-deorbiter-drag-sail-overhead.mp4" poster="kari-deorbiter-drag-sail-overhead.jpg" title="저항돛 전개시험 · 상부 촬영 (영상 12.9초)" %}
</div>

{% include section.html %}

### {% include icon.html icon="fa-solid fa-satellite-dish" %}{% include research-title.html id="optical-communications" %} {#optical-communications}

심우주 광통신은 레이저를 이용해 탐사선과 지구 사이에 데이터를 주고받는 기술입니다. 연구실은 궤적과 탐사선 자세, 지구와의 거리, 지상국의 대기·기상 조건이 통신 성능에 미치는 영향에 관심을 두고 있습니다. 통신 가능 시간과 데이터 전송량을 평가하고, 질량·전력·열 제약을 고려한 시스템 요구조건과 운용·기술실증 방안을 연구하고자 합니다.

- 거리·광학계·전력·손실을 고려한 링크 버짓과 데이터 전송 성능 분석
- 정밀 지향·포착·추적(PAT) 요구조건과 탐사선 자세 안정성 분석
- 대기·기상·가시성을 고려한 광학 지상국 배치와 통신 가용성 분석
- 전파(RF)·광통신 병행 운용, 데이터 전송 일정 및 기술실증 시나리오 설계

{% include research-figure.html topic="optical-communications" caption="탐사선에서 지상 망원경으로 보내는 레이저 링크의 개념도. 거리·지향 오차·대기 조건·통신 가능 시간이 데이터 전송 성능에 영향을 미칩니다." alt="탐사선 레이저 터미널에서 대기를 거쳐 지상 망원경으로 이어지는 하향 링크와 거리·빔 확산·지향 손실, 전력·광학계, 기상·통신 가용성, 통신 시간·데이터 전송량의 관계를 나타낸 개념도." %}

{% include section.html %}

### {% include icon.html icon="fa-solid fa-satellite" %}{% include research-title.html id="cubesat" %} {#cubesat}

큐브샛을 활용해 임무 개념과 기술을 우주에서 검증하는 방법을 연구합니다. 임무설계부터 시스템 요구조건, 지상시험, 궤도상 운용까지 이어지는 개발 과정을 다룹니다. 학생 연구원은 관련 국가연구개발사업과 연계해 연구를 수행하며, 참여 범위와 담당 업무는 연구주제와 과제 일정에 따라 정합니다.

- 큐브샛급 위성 임무 개념설계와 시스템 요구조건 도출
- 지상시험과 우주환경 적합성 검증 방법 연구
- 위성 운용개념 수립과 궤도상 기술 검증 시나리오 설계
- 국가연구개발사업과 연계한 우주실증 임무 기획

[자세 제어](#attitude-dynamics-control)와 자율제어 알고리즘은 수치 시뮬레이션에서 시작해 탑재 컴퓨터·센서·구동기를 연계한 지상시험으로 검증 범위를 넓히고, 과제 여건에 맞춰 궤도상 실증 가능성을 검토합니다.

{% include research-figure.html topic="cubesat" caption="큐브샛 임무 개념을 시스템 요구조건으로 구체화하고, 설계·제작과 지상시험을 거쳐 궤도상 운용에서 기술을 검증하는 개발 과정." alt="큐브샛 임무 개념, 시스템 설계와 제작, 지상시험, 궤도상 운용과 실증으로 이어지는 개발·검증 과정의 개념도." %}
