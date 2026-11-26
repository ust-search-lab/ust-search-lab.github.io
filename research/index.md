---
title: Research
ref: research
nav:
  order: 2
  tooltip: 연구분야
---

# {% include icon.html icon="fa-solid fa-rocket" %}Research
{: .page-title }

SEARCH Lab은 우주비행역학과 동역학계 이론을 바탕으로 지구궤도부터 심우주 탐사까지 아우르는 **우주임무 아키텍처**를 설계합니다. 궤도와 궤적 해석, 유도와 자세 제어, 수치최적화, AI와 기계학습, 시스템 분석을 결합해 임무의 실현 가능성을 평가하고 우주실증 방안을 연구합니다.
{: .page-intro }

<nav class="research-nav" aria-label="연구분야 바로가기">
  <a href="#methods">핵심 이론과 방법론</a>
  <a href="#earth-orbit">지구궤도 임무설계</a>
  <a href="#planetary">달과 행성 탐사</a>
  <a href="#entry-systems">진입, 하강, 착륙과 열방호</a>
  <a href="#solar-sail">태양돛</a>
  <a href="#optical-communications">심우주 광통신</a>
  <a href="#cubesat">큐브샛과 우주실증</a>
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

{% include research-figure.html topic="architecture" caption="임무 목표와 제약조건을 바탕으로 궤도와 궤적, 시스템, 통신 운용을 연계해 분석하고 최적화하며, 실현 가능성을 평가해 설계를 다듬습니다." alt="임무 목표와 제약조건에서 출발해 궤도·궤적과 기동, 위성·탐사선과 탑재체, 통신과 운용의 연계 모델을 구성하고, 성능, 실현 가능성, 민감도, 위험 평가를 설계에 반영하는 개념도." %}

{% include section.html %}

## 적용 연구분야 {#applications}

핵심 이론과 방법론을 다음 여섯 분야에 적용하며, 각 분야의 임무 환경과 기술 요구조건에 맞는 문제를 다룹니다.

### {% include icon.html icon="fa-solid fa-globe" %}{% include research-title.html id="earth-orbit" %} {#earth-orbit}

임무 목적에 맞는 궤도와 운용개념을 수립합니다. 지구 비구면 중력과 대기저항을 반영해 장기 궤도 변화를 예측하고, 임무 기간에 필요한 궤도유지 전략을 검토합니다.

#### 군집위성 궤도설계 {#earth-constellation}

지구관측, 통신, 기술실증을 위한 위성 수, 궤도 고도와 경사각, 궤도면과 위상 배치를 설계합니다. 관측 범위와 재방문 주기, 통신 가능 시간, 추진제 소모, 운용 부담을 비교해 임무에 적합한 구성을 찾습니다.

정밀한 상대 위치 유지가 필요한 편대비행에서는 상대궤도 동역학과 항법 오차를 반영한 [유도 및 제어](#guidance-control)를 다룹니다.

{% include research-figure.html topic="earth-constellation" caption="세 궤도면에 위성을 나누어 배치한 군집위성 개념도. 색상은 서로 다른 궤도면을 구분합니다. 설명을 위한 예시로, 크기와 거리는 축척을 따르지 않습니다." alt="지구를 둘러싼 세 원궤도에 여러 위성을 배치하고, 궤도 고도와 경사각, 궤도면, 위성 간 위상을 설계변수로 표시한 개념도." %}

#### 우주데이터센터 {#orbital-datacenter}

궤도상 데이터 저장과 처리에 필요한 전력, 열관리, 통신 조건을 통합해 실현 가능성을 검토합니다. 일조 구간과 식 구간, 위성 간 통신 및 지상 통신 기회를 바탕으로 후보 궤도와 데이터 처리 및 전송 계획을 비교합니다.

{% include section.html %}

### {% include icon.html icon="fa-solid fa-moon" %}{% include research-title.html id="planetary" %} {#planetary}

달 착륙선과 화성 궤도선, 착륙선 등 달과 행성을 탐사하는 임무를 설계합니다.

- 달 탐사 및 착륙 임무, 화성 궤도선과 착륙선의 임무 개념설계
- 탐사 목표에 따른 궤도와 착륙지 검토
- 탐사선, 표면 관측 대상, 지구 사이의 관측과 통신 기하 분석
- 관측과 통신 가능 시간을 고려한 탐사선 운용 시나리오 설계

#### 행성 간 임무설계 {#interplanetary}

지구에서 화성 같은 다른 행성으로 가는 전이궤도를 설계합니다. 출발일과 비행시간에 따른 발사에너지, 도착 조건, 발사장 제약을 함께 분석해 발사 기회를 찾고 궤적 보정 기동을 계획합니다.

{% include research-figure.html image="mars-transfer-porkchop-trajectory.jpg" width="2600" height="1167" caption="2035년 지구–화성 전이궤도 설계 예. (a) 출발일과 비행시간에 따른 발사에너지(C3) 분포와 나로우주센터 발사 가능 범위를 나타낸 포크찹 플롯, (b) 2035년 5월 출발해 12월 화성 대기권에 진입하는 전이궤도와 궤적 보정 기동(TCM)." alt="(a) 2035년 출발일을 가로축, 비행시간을 세로축으로 한 발사에너지 C3 등고선 도표에 기준 해, 최소 C3 대안, 나로우주센터 발사 가능 범위, 진입 속도 조건을 만족하는 해를 표시한 그림. (b) 태양을 중심으로 지구와 화성 궤도, 2035년 5월 26일 지구 출발부터 12월 12일 화성 진입까지의 200일 전이궤도와 네 차례의 궤적 보정 기동 지점을 표시한 그림." credit="한국항공우주연구원, 우주항공청 스페이스챌린지사업 화성 EDL 핵심기술 개발 과제" %}

#### 동역학계 이론과 다체 궤도역학 {#multi-body-dynamics}

삼체문제의 라그랑주점, 주기궤도, 불변다양체 같은 동역학 구조를 달과 행성 탐사 궤도 설계에 활용합니다.

{% include research-figure.html image="cr3bp-manifolds.png" width="2400" height="990" caption="지구–달 원형제한삼체문제의 동역학 구조. (a) 회전좌표계의 다섯 라그랑주점(L1–L5)과 주어진 에너지에서 탐사선이 들어갈 수 없는 금지영역(회색). 큰 점은 지구, 작은 점은 달입니다. (b) 달 부근 확대. L1과 L2 주위의 주기궤도(검은색)에 접근하는 안정 다양체(파란색)와 멀어지는 불안정 다양체(주황색)가 지구 영역에서 달 영역을 거쳐 바깥으로 이어지는 통로를 만듭니다. 이러한 구조가 저에너지 전이 설계의 바탕이 됩니다." alt="(a) 지구–달 회전좌표계에서 지구와 달, 라그랑주점 L1부터 L5의 위치와 고리 모양의 회색 금지영역을 나타낸 그림. 달 부근에 확대 영역이 점선 상자로 표시되어 있습니다. (b) 달 부근 확대 그림. L1과 L2 주위의 검은색 주기궤도, 왼쪽 지구 영역에서 L1 주기궤도로 들어오는 파란색 관, L1 주기궤도에서 달 쪽으로 뻗는 주황색 관, 달 쪽에서 L2 주기궤도로 들어가는 파란색 관, L2 주기궤도에서 바깥으로 나가는 주황색 관을 나타냅니다." credit="SEARCH Lab" %}

##### 지구–달 사이클러 궤도 {#cycler}

사이클러는 지구와 달 사이를 주기적으로 오가며 두 천체를 반복해서 지나가는 궤도입니다. 이상적인 모델에서는 추진 없이 왕복을 반복하므로, 지구와 달 사이의 정기 수송이나 반복 관측에 쓸 수 있는 후보 궤도가 됩니다.

SEARCH Lab은 이상적인 모델에서 안정한 사이클러가 실제 환경에서도 반복 방문을 유지할 수 있는지에 관심을 두고 있습니다. [동역학계 이론과 다체 궤도역학](#dynamical-systems)을 바탕으로 다음 문제를 연구합니다.

- 원형제한삼체문제의 사이클러 주기궤도 계산과 안정성 분석
- 달 궤도의 이심률과 태양 중력이 반복 근접통과의 지속성에 미치는 영향 평가
- 이상적인 모델의 안정성이 실제 환경의 반복 방문 유지 가능성을 얼마나 예측하는지 검토
- 실제 천체력 모델에서 반복 방문을 유지하는 궤도와 보정 기동 설계

{% include research-figure.html image="earth-moon-cyclers.png" width="2400" height="885" caption="지구–달 회전좌표계에서 본 사이클러 주기궤도 세 가지. 큰 점은 지구, 작은 점은 달이며, 거리는 지구–달 거리를 1로 둔 값입니다. 원형제한삼체문제에서 추진 없이 같은 경로를 반복하는 궤도로, 선행연구에 보고된 궤도군을 독립적으로 다시 계산했습니다. 괄호 안은 궤도군 번호, T는 주기(일)입니다." alt="지구–달 회전좌표계의 x–y 평면에 그린 세 사이클러 궤도. 주기 44.8일의 (1,1) 궤도는 지구를 크게 감싸고 달 주위에서 작은 고리를 그리며, 주기 64.3일의 (3,1) 궤도와 주기 78.9일의 (3,3) 궤도는 지구 주위를 여러 번 돌며 별 모양을 그린 뒤 달 근처를 지납니다." credit="SEARCH Lab" %}

{% include section.html %}

### {% include icon.html icon="fa-solid fa-parachute-box" %}{% include research-title.html id="entry-systems" %} {#entry-systems}

#### 화성 진입·하강·착륙 {#edl}

SEARCH Lab은 화성 탐사선이 대기권에 진입해 속도를 줄이고 지표면에 안전하게 착륙하기 위한 진입·하강·착륙(Entry, Descent, and Landing, EDL) 기술을 연구합니다. 대기 진입부터 감속과 착륙까지 단계별 핵심기술을 개발하고, 통합 시뮬레이션을 통해 전 과정의 성능을 검증하며 미래 화성 탐사를 위한 기술 기반을 마련하고 있습니다.

- 화성 대기 환경을 고려한 진입 궤적 해석과 시뮬레이션 검증
- 대기 진입을 위한 탐사선 형상 설계와 열방호 기술 개발
- 안정적인 하강을 위한 유도·제어와 낙하산 감속 기술 연구
- 정밀하고 안전한 착륙을 위한 항법·위험 회피·착륙 제어 기술 연구
- 진입부터 착륙까지 전 과정을 연계한 통합 시뮬레이션과 임무 성능 분석

{% include research-figure.html image="mars-edl-korean-lander-sequence.jpg" width="2058" height="1138" caption="한국형 화성 착륙 임무안의 EDL 시퀀스. 대기 진입부터 낙하산 전개, 동력 하강, 착지, 표면 대기 관측까지의 단계를 나타냅니다." alt="01 진입 경계점부터 02 최대 가열, 03 최대 감속, 04 극초음속 유도 비행, 05 낙하산 전개, 06 열차폐체 분리와 06A 자유낙하 탐침 10개 방출, 07 착륙 다리 전개, 08 레이더 포착과 지형상대항법, 09 후방덮개 분리와 동력 하강, 10 위험 회피, 11 수직 하강, 12 착지와 엔진 정지, 13 풍선 팽창, 14 풍선 방출, 15 라디오존데 관측으로 이어지는 15단계를 영문 라벨로 표시한 그림." credit="한국항공우주연구원, 우주항공청 스페이스챌린지사업 화성 EDL 핵심기술 개발 과제" %}

<div class="research-video-grid research-video-grid--single">
{% include research-video.html id="mars-edl-korean-lander-conops" file="mars-edl-korean-lander-conops.mp4" poster="mars-edl-korean-lander-conops.jpg" title="한국형 화성 착륙 임무의 운용 개념, 대기 진입부터 표면 임무까지 (3배속, 63초)" %}
</div>

<p class="research-video-credit">영상: 한국항공우주연구원(SEARCH Lab)</p>

##### 화성 대기 진입을 위한 열방호 소재 개발 및 시험 {#mars-tps}

화성 진입은 지구 재진입보다 진입 속도와 열유속이 낮지만 가열이 길게 이어집니다. 이러한 환경에 맞는 저밀도 삭마형 열방호 소재를 국내 기술로 개발합니다.

2026년 11월 10일 한국항공우주연구원, 한국세라믹기술원, (주)데크카본은 비츠로넥스텍의 300 kW급 아크젯 시험설비에서 열방호 소재 공동시험을 수행했습니다.

<div class="research-video-grid">
{% include research-video.html id="mars-tps-arcjet-flow" file="mars-tps-arcjet-flow.mp4" poster="mars-tps-arcjet-flow.jpg" title="아크젯 플라즈마 유동과 시편 가열 (32초)" %}
{% include research-video.html id="mars-tps-arcjet-infrared" file="mars-tps-arcjet-infrared.mp4" poster="mars-tps-arcjet-infrared.jpg" title="적외선 카메라 표면온도 계측 (21초)" %}
{% include research-video.html id="mars-tps-arcjet-side" file="mars-tps-arcjet-side.mp4" poster="mars-tps-arcjet-side.jpg" title="시편 측면 가열 장면 (32초)" %}
{% include research-video.html id="mars-tps-arcjet-front" file="mars-tps-arcjet-front.mp4" poster="mars-tps-arcjet-front.jpg" title="시편 표면 가열 장면 (32초)" %}
</div>

<p class="research-video-credit">영상: 한국항공우주연구원·한국세라믹기술원·(주)데크카본 아크젯 공동시험 (비츠로넥스텍, 2026년 11월 10일)</p>

##### 낙하산 감속 기술 연구 {#mars-parachute}

화성의 희박한 대기에서 초음속으로 낙하산을 전개해 탐사선을 감속하는 기술을 연구합니다. 연세대학교와 한국항공우주연구원은 낙하산 전개 과정에서 캐노피의 구조 응답과 주변 유동을 함께 계산하는 유체-구조 연성 해석을 수행했습니다.

<div class="research-video-grid">
{% include research-video.html id="mars-parachute-canopy-stress" file="mars-parachute-canopy-stress.mp4" poster="mars-parachute-canopy-stress.jpg" title="캐노피 응력 (16초)" %}
{% include research-video.html id="mars-parachute-flow-pressure" file="mars-parachute-flow-pressure.mp4" poster="mars-parachute-flow-pressure.jpg" title="유동 압력 (16초)" %}
{% include research-video.html id="mars-parachute-flow-density" file="mars-parachute-flow-density.mp4" poster="mars-parachute-flow-density.jpg" title="유동 밀도 (16초)" %}
{% include research-video.html id="mars-parachute-flow-velocity-z" file="mars-parachute-flow-velocity-z.mp4" poster="mars-parachute-flow-velocity-z.jpg" title="유동 z축 속도 (16초)" %}
</div>

<p class="research-video-credit">영상: 연세대학교·한국항공우주연구원, 초음속 낙하산 유체-구조 연성 해석</p>

#### 지구 재진입과 열방호시스템 {#reentry}

지구로 귀환하는 우주선과 시료귀환 캡슐이 고속으로 대기권에 진입할 때의 공력가열과 감속하중을 분석합니다. 재진입 궤적과 열환경을 함께 고려해 열차폐체 등 열방호시스템을 설계하고 검증하는 방법을 연구합니다.

- 재진입 궤적, 진입 회랑, 시료귀환 캡슐 회수 시나리오 설계
- 공력가열과 감속하중 등 재진입 환경 예측
- 열방호시스템 개념설계와 두께 산정, 삭마형 및 재사용형 열방호재의 열응답 해석
- 아크젯 등 지상시험과 비행시험을 활용한 검증 방법 연구

{% include research-figure.html topic="reentry" caption="시료귀환 캡슐의 단면 개념도. 이탈 충격파와 고온 충격층, 정체점 가열, 전방동체 삭마재와 후방동체 열방호재의 구성을 나타내며, 오른쪽 확대도는 삭마재 내부의 온도 분포와 두께 산정 기준인 접합면 온도 한계를 보여줍니다. 형상과 두께는 축척을 따르지 않습니다." alt="극초음속 유동과 이탈 충격파를 마주한 시료귀환 캡슐의 단면. 정체점, 전방동체 삭마재, 후방동체 열방호재, 구조체, 시료 용기를 구분하고, 확대도에 탄화층, 열분해층, 미반응층, 접합층, 구조체의 적층과 온도 분포를, 아래에 재진입 궤적부터 공력가열 환경, 열방호시스템 두께 산정, 아크젯 시험과 비행시험까지의 해석 흐름을 나타낸 개념도." %}

{% include section.html %}

### {% include icon.html icon="fa-solid fa-sun" %}{% include research-title.html id="solar-sail" %} {#solar-sail}

태양돛은 햇빛이 돛에 운동량을 전달할 때 생기는 태양복사압을 이용해 추력을 얻습니다. 돛의 방향을 조절해 궤적을 바꾸는 원리를 바탕으로, 추진제 사용을 줄이는 장기 비행과 미래 심우주 탐사 임무를 설계합니다.

- 태양복사압과 돛 자세를 고려한 우주비행역학
- 태양돛 기반 궤도상승과 장기 저추력 궤적 설계
- 비케플러 궤도 등 특수궤도와 미래 탐사 임무 개념설계
- 태양돛 우주실증 임무 기획

#### 태양돛을 활용한 심우주 탐사 {#solar-sail-deep-space}

태양돛은 추진제를 쓰지 않고 오랫동안 가속할 수 있어 비행 기간이 긴 심우주 탐사에 유리합니다. SEARCH Lab은 태양돛 우주선의 화성 탐사를 중심으로 지구 출발부터 화성 도착 이후의 운용까지 연구합니다.

- 지구에서 화성으로 가는 태양돛 전이궤도 최적화
- 화성 대기 진입 조건을 고려한 태양돛 우주선의 도착 조건 분석
- 화성 궤도 진입 이후의 궤도 유지와 자세 안정화
- 태양돛을 이용한 화성 궤도 장기 운용

관련 논문: [Solar sail-based energy-efficient architecture for long-term Mars orbit operations (2026)](https://doi.org/10.1016/j.ast.2026.111779), [Analysis of Mars Arrival Conditions for Solar Sail Spacecraft Considering Entry Interface Constraints (2026)](https://ksss.or.kr/society/tksss/media?key=tksss/bulletin/2026spring35_1.pdf)

#### 자세와 궤도 통합 제어 {#integrated-attitude-orbit-control}

[유도 및 제어](#optimization)와 [자세 역학과 자세 제어](#attitude-dynamics-control)를 결합해 태양돛의 궤도와 자세 운동을 함께 해석하고 제어하는 방법을 연구합니다. 태양복사압에 의한 힘과 토크, 질량중심과 압력중심의 관계를 모델링하고, 구동기 한계, 관측 및 통신을 위한 지향 조건을 반영한 6자유도 시뮬레이션으로 임무 수행 가능성을 평가합니다. [AI와 기계학습](#ai-machine-learning)을 활용한 제어 명령 예측과 자율비행의 적용 가능성도 검토합니다.

관련 선행연구: [딥러닝 기반 태양돛 최적제어의 간접법 해석 (2025)](https://www.dbpia.co.kr/journal/articleDetail?nodeId=NODE12589746)

#### 태양돛 전개장치 개발 및 지상시험 {#solar-sail-ground-test}

한국항공우주연구원은 심우주 탐사에 활용할 태양돛 전개기술을 확보하기 위해 10 m × 10 m(100 m²) 규모의 지상 시험모델을 개발했습니다. 모터로 네 개의 지지대(붐)를 펼치면서 수납된 얇은 돛을 전개하는 구조로, 지상시험을 통해 붐과 돛의 전개 과정에서 발생하는 문제와 개선점을 확인했습니다. 아래 영상은 시험모델의 전개 과정을 상부와 측면에서 촬영한 것입니다.

관련 자료: [한국항공우주연구원 보도자료](https://www.kari.re.kr/kor/article/ATCL87374b48c/18228), [태양돛 전개 시험 및 교훈](https://doi.org/10.52912/jsta.2026.6.3.293)

<div class="research-video-grid">
{% include research-video.html id="sail-test-overhead" file="kari-solar-sail-deployment-overhead.mp4" poster="kari-solar-sail-deployment-overhead.jpg" title="태양돛 전개시험, 상부 촬영 (23초)" %}
{% include research-video.html id="sail-test-side" file="kari-solar-sail-deployment-side.mp4" poster="kari-solar-sail-deployment-side.jpg" title="태양돛 전개시험, 측면 촬영 (22초)" %}
</div>

#### 우주쓰레기 제거용 궤도이탈 장치 개발 및 지상시험 {#deorbiter-ground-test}

한국항공우주연구원은 저궤도 우주쓰레기의 포획과 제거 기술을 검증하기 위해 궤도이탈 장치(deorbiter)의 지상 시험모델을 개발했습니다. 견인부, 포획부, 전개부로 구성되며, 5 m × 5 m(25 m²)의 저항돛(drag sail)을 펼쳐 대기저항을 높이고 포획한 물체의 대기권 재진입을 유도하는 개념입니다. 아래 영상은 이 가운데 저항돛의 전개 기능을 확인하는 지상시험 장면입니다.

관련 자료: [한국항공우주연구원 보도자료](https://www.kari.re.kr/kor/article/ATCL87374b48c/18417), [궤도이탈 장치 개발과 시험 논문](https://doi.org/10.52912/jsta.2026.6.2.196)

<div class="research-video-grid">
{% include research-video.html id="deorbiter-test-wide" file="kari-deorbiter-drag-sail-wide.mp4" poster="kari-deorbiter-drag-sail-wide.jpg" title="저항돛 전개시험, 전체 모습 (2.4초)" %}
{% include research-video.html id="deorbiter-test-overhead" file="kari-deorbiter-drag-sail-overhead.mp4" poster="kari-deorbiter-drag-sail-overhead.jpg" title="저항돛 전개시험, 상부 촬영 (12.9초)" %}
</div>

{% include section.html %}

### {% include icon.html icon="fa-solid fa-satellite-dish" %}{% include research-title.html id="optical-communications" %} {#optical-communications}

심우주 광통신은 레이저를 이용해 탐사선과 지구 사이에 데이터를 주고받는 기술입니다. 연구실은 궤적과 탐사선 자세, 지구와의 거리, 지상국의 대기와 기상 조건이 통신 성능에 미치는 영향을 분석합니다. 통신 가능 시간과 데이터 전송량을 평가하고, 질량, 전력, 열 제약을 고려한 시스템 요구조건과 운용 및 기술실증 방안을 연구합니다.

- 거리, 광학계, 전력, 손실을 고려한 링크 버짓과 데이터 전송 성능 분석
- 정밀 지향, 포착 및 추적(PAT) 요구조건과 탐사선 자세 안정성 분석
- 대기와 기상 조건, 가시성을 고려한 광학 지상국 배치와 통신 가용성 분석
- 전파(RF)와 광통신 병행 운용, 데이터 전송 일정 및 기술실증 시나리오 설계

{% include research-figure.html topic="optical-communications" caption="탐사선에서 지상 망원경으로 보내는 레이저 링크의 개념도. 거리, 지향 오차, 대기 조건, 통신 가능 시간이 데이터 전송 성능에 영향을 미칩니다." alt="탐사선 레이저 터미널에서 대기를 거쳐 지상 망원경으로 이어지는 하향 링크와 거리, 빔 확산과 지향 손실, 전력과 광학계, 기상 조건과 통신 가용성, 통신 시간과 데이터 전송량의 관계를 나타낸 개념도." %}

#### 화성–지구 광통신 링크의 수신기 모델 분석 {#mars-optical-downlink}

화성과 지구 사이의 광통신 하향링크는 펄스 하나에 도달하는 광자가 매우 적어, 수신기를 어떤 통계 모델로 나타내는지에 따라 링크 버짓의 결론이 달라질 수 있습니다. SEARCH Lab은 펄스위치변조(M-PPM)를 쓰는 화성–지구 하향링크에서 광학 링크 조건을 고정하고, 애벌란시 광다이오드(APD) 가우시안 모델과 이상적인 포아송 광자계수 모델을 비교했습니다. 같은 조건에서 필요한 신호 광자 수는 모델에 따라 4.7~6.2배 달라졌고, 그 차이는 확률분포의 모양보다 검출기 잡음 모델에서 비롯했습니다. 이 값은 모델 선택에 따른 민감도이며, 실제 검출기의 성능 차이를 뜻하지 않습니다.

{% include research-figure.html image="mars-optical-receiver-models.png" width="2000" height="1428" caption="펄스당 신호 광자 수에 따른 부호화 전 비트오류율. 실선은 APD 가우시안 수신기 모델, 점선은 이상적인 포아송 광자계수 모델이고 M은 PPM 차수입니다. 같은 오류율에 필요한 광자 수가 수신기 모델에 따라 달라집니다." alt="가로축은 펄스당 신호 광자 수, 세로축은 부호화 전 비트오류율인 로그 그래프. PPM 차수 16, 64, 256에 대해 APD 가우시안 모델의 실선 세 개와 이상적인 포아송 모델의 점선 세 개가 그려져 있으며, 점선이 실선보다 더 적은 광자 수에서 오류율이 떨어집니다." credit="박재익, Optical and Quantum Electronics 게재 승인 논문 (2026)" %}

관련 논문: Jae-ik Park, "Decomposing Receiver-Model Sensitivity in M-PPM Mars–Earth Optical Downlinks: APD Gaussian and Ideal Poisson Models," *Optical and Quantum Electronics*, 게재 승인 (2026). [Publications]({{ '/publications/' | relative_url }})

{% include section.html %}

### {% include icon.html icon="fa-solid fa-satellite" %}{% include research-title.html id="cubesat" %} {#cubesat}

큐브샛을 활용해 임무 개념과 기술을 우주에서 검증하는 방법을 연구합니다. 임무설계부터 시스템 요구조건, 지상시험, 궤도상 운용까지 이어지는 개발 과정을 다룹니다. 학생연구원은 관련 국가연구개발사업과 연계해 연구를 수행하며, 참여 범위와 담당 업무는 연구주제와 과제 일정에 따라 정합니다.

- 큐브샛급 위성 임무 개념설계와 시스템 요구조건 도출
- 지상시험과 우주환경 적합성 검증 방법 연구
- 위성 운용개념 수립과 궤도상 기술 검증 시나리오 설계
- 국가연구개발사업과 연계한 우주실증 임무 기획

[자세 제어](#attitude-dynamics-control)와 자율제어 알고리즘은 수치 시뮬레이션에서 시작해 탑재 컴퓨터, 센서, 구동기를 연계한 지상시험으로 검증 범위를 넓히고, 과제 여건에 맞춰 궤도상 실증 가능성을 검토합니다.

{% include research-figure.html topic="cubesat" caption="큐브샛 임무 개념을 시스템 요구조건으로 구체화하고, 설계, 제작, 지상시험을 거쳐 궤도상 운용에서 기술을 검증하는 개발 과정." alt="큐브샛 임무 개념, 시스템 설계와 제작, 지상시험, 궤도상 운용과 실증으로 이어지는 개발과 검증 과정의 개념도." %}
