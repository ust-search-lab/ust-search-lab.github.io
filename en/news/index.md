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

<div class="news-actions">
  <a class="action-button" href="{{ '/admin/' | relative_url }}#/collections/news/new">{% include icon.html icon="fa-solid fa-pen-to-square" %}Write a news post</a>
  <a class="text-link" href="{{ '/admin/' | relative_url }}#/collections/news">Edit existing posts</a>
</div>
<p class="news-edit-help">Select “Edit post” to open that post in the editor. Sign in with an administrator GitHub account, make your changes, then choose Publish → Publish now.</p>

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
