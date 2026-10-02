---
title: People
ref: people
nav:
  order: 3
  tooltip: 구성원
---

# {% include icon.html icon="fa-solid fa-users" %}People

{% include section.html %}

## 책임교수

{% include list.html data="members" component="portrait" filter="role == 'principal-investigator' && lang == 'ko'" %}

{% comment %} collaborating researchers: hidden for now

{% include section.html %}

## 공동연구진

SEARCH Lab은 우주탐사 아키텍처와 우주임무설계를 중심으로, 구조·전개 시스템, 위성자료 처리, 유도항법제어, 태양돛 기술 등 다양한 전문분야의 연구진과 함께 미래 우주임무를 연구합니다. 학생 연구자는 각 분야 전문가와의 공동연구를 통해 우주임무의 설계, 구현, 검증 과정을 폭넓게 경험할 수 있습니다.

{% include list.html data="members" component="portrait" filter="role == 'collaborator' && lang == 'ko'" %}

{% endcomment %}

{% include section.html %}

## 학생 연구자

SEARCH Lab에서 함께 연구할 석·박사과정 학생 연구자에 관한 안내는 [For Students]({{ "students/" | relative_url }}) 페이지를 참고하세요.
