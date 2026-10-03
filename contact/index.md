---
title: Contact
ref: contact
description: SEARCH Lab의 석·박사과정 진학과 학생 연구 참여에 관심 있는 분들을 위한 문의 안내입니다.
nav:
  order: 7
  tooltip: 학생 모집·지원 문의
---

# {% include icon.html icon="fa-regular fa-envelope" %}Contact
{: .page-title }

{% assign inquiry_subject = '[SEARCH Lab] 학생 진학·연구 참여 문의' | uri_escape %}

<div class="contact-recruitment">
  <div class="contact-intro">
    <p class="contact-eyebrow">학생 연구자 모집</p>
    <h2>우주임무 설계와 기술실증에 함께할 학생 연구자를 기다립니다.</h2>
    <p>SEARCH Lab의 석·박사과정 진학에 관심이 있다면, 관심 연구분야와 진학 계획을 담아 이메일로 문의해 주세요.</p>
    <p class="contact-welcome"><strong>군위탁장교의 석·박사과정 진학도 환영합니다.</strong></p>
  </div>
  <div class="contact-email-card">
    <h3>진학·연구 참여 문의</h3>
    <p class="contact-person">박재익 교수<span>UST · 한국항공우주연구원</span></p>
    <a class="contact-button action-button" href="mailto:{{ site.links.email | escape }}?subject={{ inquiry_subject }}"><span aria-hidden="true">{% include icon.html icon="fa-regular fa-envelope" %}</span>이메일로 문의하기</a>
  </div>
</div>

<div class="contact-guidance" markdown="1">

## 문의할 때 알려주세요

아래 내용을 간단히 소개해 주시면 상담에 도움이 됩니다.

{: .contact-checklist }
- **관심 과정과 시기** — 희망하는 학위과정과 입학 시기
- **전공과 학업 배경** — 현재 전공과 재학·졸업 여부, 관련 학습 경험
- **관심 연구주제** — 해보고 싶은 연구와 관련 연구·프로젝트 경험이 있다면 소개

</div>

<div class="contact-security" markdown="1">

## 연구원 출입·보안 안내

교육과 연구가 이루어지는 UST 한국항공우주연구원 캠퍼스는 [국가보안 ‘나’급에 해당하는 국책연구보안시설](https://www.kari.re.kr/kor/contents/4)입니다.

연구원 출입 및 연구 참여를 위해서는 관련 규정에 따른 신원 확인 등 보안 절차를 충족해야 하며, 해당 절차상 결격사유가 없어야 합니다. 세부 적용 기준과 절차는 UST 및 한국항공우주연구원의 안내를 따릅니다.

</div>

<div class="contact-location" aria-labelledby="contact-location-title">
  <h2 id="contact-location-title">찾아오시는 길</h2>
  <div class="contact-location-grid">
    <div class="contact-location-info">
      <p class="contact-location-name">UST 한국항공우주연구원 캠퍼스</p>
      <address>대전광역시 유성구 과학로 169-84<br>한국항공우주연구원 · 우편번호 34133</address>
      <p class="contact-visit-note">방문 전 이메일로 일정을 협의해 주세요. 연구원 방문에는 사전 출입 신청이 필요합니다.</p>
      <a class="action-button" href="https://map.kakao.com/link/to/한국항공우주연구원,36.37553137609033,127.35476898110238" target="_blank" rel="noopener noreferrer"><span aria-hidden="true">{% include icon.html icon="fa-solid fa-map-location-dot" %}</span>카카오맵 길찾기</a>
      <div class="contact-links">
        <a class="text-link" href="https://www.kari.re.kr/kor/contents/5" target="_blank" rel="noopener noreferrer">항우연 공식 교통 안내 <span aria-hidden="true">↗</span></a>
      </div>
    </div>
    <iframe class="contact-map" title="한국항공우주연구원 대전 본원 위치 지도" src="https://www.openstreetmap.org/export/embed.html?bbox=127.34477%2C36.36953%2C127.36477%2C36.38153&amp;layer=mapnik&amp;marker=36.37553137609033%2C127.35476898110238" width="600" height="320" loading="lazy" referrerpolicy="strict-origin-when-cross-origin"></iframe>
  </div>
</div>

<div class="contact-explore">
  <p>연구분야와 학생 연구자의 학습·연구 과정을 살펴보세요.</p>
  <div class="contact-links">
    <a class="text-link" href="{{ '/students/' | relative_url }}">학생 연구자 안내 <span aria-hidden="true">→</span></a>
    <a class="text-link" href="{{ '/research/' | relative_url }}">연구분야 살펴보기 <span aria-hidden="true">→</span></a>
  </div>
</div>
