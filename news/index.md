---
title: News
ref: news
nav:
  order: 6
  tooltip: 연구실 소식
---

# {% include icon.html icon="fa-solid fa-newspaper" %}News
{: .page-title }

SEARCH Lab의 공지사항과 연구실 소식을 전합니다.
{: .page-intro }

<p><a class="action-button" href="{{ '/admin/' | relative_url }}#/collections/news/new">{% include icon.html icon="fa-solid fa-pen-to-square" %}공지사항 작성</a></p>

<p class="news-external-link"><a class="text-link" href="{{ '/space-news/' | relative_url }}">국내외 우주탐사 뉴스 <span aria-hidden="true">→</span></a></p>

{% include section.html %}

{% assign news = site.posts | where: "lang", "ko" %}
{% if news.size == 0 %}
아직 등록된 소식이 없습니다.
{: .page-empty }
{% else %}
## 최근 소식

{% include search-box.html %}

{% include search-info.html %}

{% include list.html data="posts" component="post-excerpt" filter="lang == 'ko'" %}
{% endif %}
