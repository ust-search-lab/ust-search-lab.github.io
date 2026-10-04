---
title: Contact
ref: contact
description: SEARCH Lab의 석·박사과정 진학·연구 참여 문의와 방문 안내입니다.
nav:
  order: 8
  tooltip: 진학·연구 참여 문의
---

# {% include icon.html icon="fa-regular fa-envelope" %}Contact
{: .page-title }

{% assign inquiry_subject = '[SEARCH Lab] 학생 진학·연구 참여 문의' | uri_escape %}

<div class="contact-recruitment">
  <div class="contact-intro">
    <p class="contact-eyebrow">학생 연구자 모집</p>
    <h2>우주임무 설계와 기술실증을 연구할 학생을 모집합니다.</h2>
    <p>석·박사과정 진학에 관심이 있는 분은 관심 연구분야와 입학 희망 시기를 적어 이메일로 문의해 주세요.</p>
    <p class="contact-welcome"><strong>군위탁장교의 석·박사과정 진학도 환영합니다.</strong></p>
  </div>
  <div class="contact-email-card">
    <h3>진학·연구 참여 문의</h3>
    <p class="contact-person">박재익 교수<span>UST · 한국항공우주연구원</span></p>
    <a class="contact-button action-button" href="mailto:{{ site.links.email | escape }}?subject={{ inquiry_subject }}"><span aria-hidden="true">{% include icon.html icon="fa-regular fa-envelope" %}</span>이메일로 문의하기</a>
  </div>
</div>

<div class="contact-guidance" markdown="1">

## 문의 메일에 담을 내용

다음 내용을 간단히 소개해 주세요.

{: .contact-checklist }
- **진학 계획** — 희망하는 학위과정과 입학 시기
- **학업 배경** — 전공, 재학·졸업 여부, 관련 학습 경험
- **연구 관심** — 관심 있는 연구주제. 관련 연구·프로젝트 경험이 있다면 함께 알려주세요.

</div>

<div class="contact-security" markdown="1">

## 연구원 출입·보안 안내

SEARCH Lab이 위치한 한국항공우주연구원은 [국가보안 ‘나’급에 해당하는 국책연구보안시설](https://www.kari.re.kr/kor/contents/4)입니다.

연구원 출입과 연구 참여를 위해서는 신원 확인 등 관련 보안 절차를 거쳐야 하며, 규정에 따른 결격사유가 없어야 합니다. 자세한 기준과 절차는 UST와 한국항공우주연구원의 안내를 따릅니다.

</div>

<div class="contact-location" aria-labelledby="contact-location-title">
  <h2 id="contact-location-title">찾아오시는 길</h2>
  <div class="contact-location-grid">
    <div class="contact-location-info">
      <p class="contact-location-name">UST 한국항공우주연구원 캠퍼스</p>
      <address>대전광역시 유성구 과학로 169-84<br>한국항공우주연구원 · 우편번호 34133</address>
      <p class="contact-visit-note">방문을 원하시면 먼저 이메일로 일정을 협의해 주세요. 연구원 출입은 사전 신청이 필요합니다.</p>
      <a class="action-button" href="https://map.kakao.com/link/to/한국항공우주연구원,36.37553137609033,127.35476898110238" target="_blank" rel="noopener noreferrer"><span aria-hidden="true">{% include icon.html icon="fa-solid fa-map-location-dot" %}</span>카카오맵 길찾기</a>
      <div class="contact-links">
        <a class="text-link" href="https://www.kari.re.kr/kor/contents/5" target="_blank" rel="noopener noreferrer">한국항공우주연구원 교통 안내 <span aria-hidden="true">↗</span></a>
      </div>
    </div>
    <iframe class="contact-map" title="한국항공우주연구원 대전 본원 위치 지도" src="https://www.openstreetmap.org/export/embed.html?bbox=127.34477%2C36.36953%2C127.36477%2C36.38153&amp;layer=mapnik&amp;marker=36.37553137609033%2C127.35476898110238" width="600" height="320" loading="lazy" referrerpolicy="strict-origin-when-cross-origin"></iframe>
  </div>
</div>

<div class="contact-explore">
  <p>연구분야와 학생 안내도 함께 참고해 주세요.</p>
  <div class="contact-links">
    <a class="text-link" href="{{ '/students/' | relative_url }}">학생 연구자 안내 <span aria-hidden="true">→</span></a>
    <a class="text-link" href="{{ '/research/' | relative_url }}">연구분야 살펴보기 <span aria-hidden="true">→</span></a>
  </div>
</div>
