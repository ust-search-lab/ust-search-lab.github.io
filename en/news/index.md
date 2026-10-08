---
title: News
ref: news
nav:
  order: 6
  tooltip: Lab news
---

# {% include icon.html icon="fa-solid fa-newspaper" %}News
{: .page-title }

Announcements and news from SEARCH Lab.
{: .page-intro }

<p class="news-external-link"><a class="text-link" href="{{ '/en/space-news/' | relative_url }}">Space news from Korea and around the world <span aria-hidden="true">→</span></a></p>

{% include section.html %}

{% assign news = site.posts | where: "lang", "en" %}
{% if news.size == 0 %}
No news yet.
{: .page-empty }
{% else %}
## Latest news

{% include search-box.html %}

{% include search-info.html %}

{% include list.html data="posts" component="post-excerpt" filter="lang == 'en'" %}
{% endif %}
