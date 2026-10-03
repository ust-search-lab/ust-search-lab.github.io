---
title: News
ref: news
nav:
  order: 6
  tooltip: Lab news
---

# {% include icon.html icon="fa-solid fa-newspaper" %}News
{: .page-title }

News and updates from SEARCH Lab.
{: .page-intro }

{% include section.html %}

{% assign news = site.posts | where: "lang", "en" %}
{% if news.size == 0 %}
No news yet.
{: .page-empty }
{% else %}
{% include search-box.html %}

{% include search-info.html %}

{% include list.html data="posts" component="post-excerpt" filter="lang == 'en'" %}
{% endif %}
