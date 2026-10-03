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

{% comment %} collaborating researchers: hidden for now

{% include section.html %}

## Collaborating Researchers

SEARCH Lab collaborates on space exploration architecture and mission design with researchers in structures and deployable systems; satellite data processing; guidance, navigation, and control; and solar sail technology. These collaborations give students experience in designing, implementing, and verifying space missions.

{% include list.html data="members" component="portrait" filter="role == 'collaborator' && lang == 'en'" %}

{% endcomment %}

{% include section.html %}

## Student Researchers

To learn about joining SEARCH Lab as a master's or doctoral student, visit our [student information page]({{ "en/students/" | relative_url }}).
