---
title: News
ref: news
nav:
  order: 6
  tooltip: Lab news
---

# {% include icon.html icon="fa-solid fa-newspaper" %}News

News from SEARCH Lab.

{% include section.html %}

{% assign news = site.posts | where: "lang", "en" %}
{% if news.size == 0 %}
No news yet.
{:.center}
{% else %}
{% include search-box.html %}

{% include search-info.html %}

{% include list.html data="posts" component="post-excerpt" filter="lang == 'en'" %}
{% endif %}
