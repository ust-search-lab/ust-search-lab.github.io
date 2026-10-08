---
title: People
ref: people
nav:
  order: 3
  tooltip: Our team
---

# {% include icon.html icon="fa-solid fa-users" %}People
{: .page-title }

{% include section.html %}

## Principal Investigator

{% assign investigators = site.members | where: "role", "principal-investigator" | where: "lang", page.lang %}
{% for investigator in investigators %}
  {% include principal-investigator.html member=investigator mode="summary" %}
{% endfor %}

{% include section.html %}

## Collaborators

{% assign collaborators = site.members | where: "role", "collaborator" | where: "lang", page.lang | where_exp: "member", "member.published != false" %}
{% for collaborator in collaborators %}
  {% include collaborator.html member=collaborator mode="summary" %}
{% endfor %}

{% include section.html %}

## Student Researchers

To learn about joining SEARCH Lab as a master's or doctoral student, visit [For Students]({{ "en/students/" | relative_url }}).
