---
title: People
ref: people
nav:
  order: 3
  tooltip: 구성원
---

# {% include icon.html icon="fa-solid fa-users" %}People
{: .page-title }

{% include section.html %}

## 책임교수

{% assign investigators = site.members | where: "role", "principal-investigator" | where: "lang", page.lang %}
{% for investigator in investigators %}
  {% include principal-investigator.html member=investigator mode="summary" %}
{% endfor %}

{% comment %} collaborating researchers: hidden for now

{% include section.html %}

## 공동연구진

SEARCH Lab은 우주탐사 아키텍처와 임무설계를 중심으로 구조·전개 시스템, 위성자료 처리, 유도항법제어, 태양돛 기술 등 다양한 분야의 연구진과 협력합니다. 학생 연구자는 각 분야 전문가와 공동연구를 수행하며 우주임무의 설계, 구현, 검증 과정을 폭넓게 경험할 수 있습니다.

{% include list.html data="members" component="portrait" filter="role == 'collaborator' && lang == 'ko'" %}

{% endcomment %}

{% include section.html %}

## 학생 연구자

SEARCH Lab에서 석·박사과정 연구에 참여하려면 [학생 연구자 안내]({{ "students/" | relative_url }}) 페이지를 참고하세요.
