---
title: News
ref: news
nav:
  order: 6
  tooltip: 연구실 소식
---

# {% include icon.html icon="fa-solid fa-newspaper" %}News
{: .page-title }

SEARCH Lab의 소식을 전합니다.
{: .page-intro }

{% include section.html %}

{% assign news = site.posts | where: "lang", "ko" %}
{% if news.size == 0 %}
아직 등록된 소식이 없습니다.
{: .page-empty }
{% else %}
{% include search-box.html %}

{% include search-info.html %}

{% include list.html data="posts" component="post-excerpt" filter="lang == 'ko'" %}
{% endif %}
