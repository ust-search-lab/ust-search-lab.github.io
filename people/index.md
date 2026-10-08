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

{% include section.html %}

## 협력 연구원

{% assign collaborators = site.members | where: "role", "collaborator" | where: "lang", page.lang | where_exp: "member", "member.published != false" %}
{% for collaborator in collaborators %}
  {% include collaborator.html member=collaborator mode="summary" %}
{% endfor %}

{% include section.html %}

## 학생 연구원

SEARCH Lab에서 석·박사과정 연구에 참여하려면 [학생 연구원 안내]({{ "students/" | relative_url }}) 페이지를 참고하세요.
