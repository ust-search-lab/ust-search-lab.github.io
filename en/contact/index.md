---
title: Contact
ref: contact
description: Contact SEARCH Lab about master's and doctoral study, student research opportunities, and visits.
nav:
  order: 8
  tooltip: Prospective student inquiries
---

# {% include icon.html icon="fa-regular fa-envelope" %}Contact
{: .page-title }

{% assign inquiry_subject = '[SEARCH Lab] Prospective student inquiry' | uri_escape %}

<div class="contact-recruitment">
  <div class="contact-intro">
    <p class="contact-eyebrow">Graduate student recruitment</p>
    <h2>We are recruiting students in space mission design and technology demonstration.</h2>
    <p>If you are interested in master's or doctoral study at SEARCH Lab, please email us with your research interests and preferred start date.</p>
    <p class="contact-welcome"><strong>Military officers pursuing master's or doctoral study through military-sponsored education programs are also welcome.</strong></p>
  </div>
  <div class="contact-email-card">
    <h3>Graduate study &amp; research inquiries</h3>
    <p class="contact-person">Professor Jae-ik Park<span>UST · Korea Aerospace Research Institute (KARI)</span></p>
    <a class="contact-button action-button" href="mailto:{{ site.links.email | escape }}?subject={{ inquiry_subject }}"><span aria-hidden="true">{% include icon.html icon="fa-regular fa-envelope" %}</span>Email Professor Park</a>
  </div>
</div>

<div class="contact-guidance" markdown="1">

## What to include in your email

Please briefly introduce yourself and include the following.

{: .contact-checklist }
- **Study plans** — Your intended degree and preferred start date
- **Academic background** — Your field of study, whether you are currently studying or have graduated, and relevant coursework
- **Research interests** — Topics you would like to study. If you have relevant research or project experience, please describe it briefly.

</div>

<div class="contact-security" markdown="1">

## Campus access and security

SEARCH Lab is based at the Korea Aerospace Research Institute, a [national security facility in the “Na” (나급) category](https://www.kari.re.kr/kor/contents/4).

Campus access and research participation require identity verification and other security procedures under applicable regulations. You must meet the relevant requirements and have no grounds for disqualification. Please follow UST and KARI guidance for detailed requirements and procedures.

</div>

<div class="contact-location" aria-labelledby="contact-location-title">
  <h2 id="contact-location-title">Location &amp; directions</h2>
  <div class="contact-location-grid">
    <div class="contact-location-info">
      <p class="contact-location-name">UST KARI School</p>
      <address>Korea Aerospace Research Institute<br>169-84, Gwahak-ro, Yuseong-gu<br>Daejeon 34133, Republic of Korea</address>
      <p class="contact-visit-note">Please email us to arrange a visit. Entry to KARI requires advance registration.</p>
      <a class="action-button" href="https://map.kakao.com/link/to/KARI,36.37553137609033,127.35476898110238" target="_blank" rel="noopener noreferrer"><span aria-hidden="true">{% include icon.html icon="fa-solid fa-map-location-dot" %}</span>Directions on Kakao Map</a>
      <div class="contact-links">
        <a class="text-link" href="https://www.kari.re.kr/kor/contents/5" target="_blank" rel="noopener noreferrer">KARI travel information (Korean) <span aria-hidden="true">↗</span></a>
      </div>
    </div>
    <iframe class="contact-map" title="Map of KARI headquarters in Daejeon" src="https://www.openstreetmap.org/export/embed.html?bbox=127.34477%2C36.36953%2C127.36477%2C36.38153&amp;layer=mapnik&amp;marker=36.37553137609033%2C127.35476898110238" width="600" height="320" loading="lazy" referrerpolicy="strict-origin-when-cross-origin"></iframe>
  </div>
</div>

<div class="contact-explore">
  <p>See our research areas and guidance for prospective students.</p>
  <div class="contact-links">
    <a class="text-link" href="{{ '/en/students/' | relative_url }}">For Students <span aria-hidden="true">→</span></a>
    <a class="text-link" href="{{ '/en/research/' | relative_url }}">Explore our research <span aria-hidden="true">→</span></a>
  </div>
</div>
