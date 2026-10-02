---
title: People
ref: people
nav:
  order: 3
  tooltip: Our team
---

# {% include icon.html icon="fa-solid fa-users" %}People

{% include section.html %}

## Principal Investigator

{% include list.html data="members" component="portrait" filter="role == 'principal-investigator' && lang == 'en'" %}

{% comment %} collaborating researchers: hidden for now

{% include section.html %}

## Collaborating Researchers

Centered on space exploration architecture and space mission design, SEARCH Lab studies future space missions together with researchers from diverse fields, including structures and deployable systems, satellite data processing, guidance, navigation, and control, and solar sail technology. Through collaboration with experts in each field, student researchers gain broad experience in the design, implementation, and verification of space missions.

{% include list.html data="members" component="portrait" filter="role == 'collaborator' && lang == 'en'" %}

{% endcomment %}

{% include section.html %}

## Student Researchers

For information on joining SEARCH Lab as a master's or doctoral student, see the [For Students]({{ "en/students/" | relative_url }}) page.
