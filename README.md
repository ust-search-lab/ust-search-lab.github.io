![on-push](../../actions/workflows/on-push.yaml/badge.svg)
![on-pull-request](../../actions/workflows/on-pull-request.yaml/badge.svg)
![on-schedule](../../actions/workflows/on-schedule.yaml/badge.svg)

# SEARCH Lab Website

Official website of SEARCH Lab (Space Exploration ARCHitecture Laboratory) at UST.

Visit **[ust-search-lab.github.io](https://ust-search-lab.github.io)**

_Built with [Lab Website Template](https://greene-lab.gitbook.io/lab-website-template-docs) v1.4.0_

## Site structure (Korean / English)

- Korean pages live at the root (`/`, `/about/`, ...) and English pages under `/en/` (`/en/`, `/en/about/`, ...).
  The language comes from the `lang` front matter (default `ko`, `en` for everything under `en/`).
- Each page and member profile has a `ref` key. The language switch in the header links to the page with the same `ref` in the other language.
- Member profiles are in `_members/`, one file per language (`name.md` with `lang: ko`, `name-en.md` with `lang: en`).
- Interface text for both languages is in `_data/i18n.yaml`.
- Links pages (`/links/` and `/en/links/`) share `_data/resource-links.yaml`
  and `_includes/resource-links.html`, with page styles in `_styles/links.scss`.
  Keep descriptions in both languages and use official destination URLs.
  Institution entries resolve their names and URLs from `_data/institutions.yaml`,
  which is also used by the footer. Links appears between News and Contact.
- Both home pages use `_includes/home.html`, with bilingual copy in
  `_data/home.yaml` and styles scoped to `main[data-page="home"]` in
  `_styles/home.scss`. `_data/research-topics.yaml` provides the six core
  theories and methods in this presentation order: astrodynamics and orbit
  analysis, dynamical systems, guidance/control and numerical optimization,
  attitude dynamics and control, AI/machine learning, and mission architecture
  and systems analysis. Home and Research render this same
  ordered list; Research uses its bilingual summaries, and For Students uses
  the same titles with each method's bilingual `study` topics. About's inline
  method/application lists use `_includes/research-topic-names.html` to keep
  the names aligned. The six application
  areas start with Earth-Orbit Mission Design. Home cards, Research headings,
  and student research-area links share these application titles and ordering.
  `_includes/research-title.html` resolves application headings by topic ID
  rather than array position. Keep each topic ID aligned with its Research
  anchor; optional method aliases preserve earlier anchors. Constellation design
  is a subsection of `earth-orbit`, and integrated attitude/orbit control is
  detailed within `solar-sail` as an application of the shared methods.
  `_data/home-images.yaml` supplies the cards' mission photographs and illustrations,
  bilingual captions and alternative text, and links to the official image
  sources. Captions identify illustrations explicitly; provenance records the
  verified source and credit. The constellation card uses an original SVG of
  multiple orbital planes and satellite positions, with an annotated version
  on the Research pages. The earlier concept SVGs for other topics remain unused.
  Below the introduction, each home page displays the three latest posts in
  its language, including publication dates, titles, and excerpts linking to
  the full announcements. Adding a post to `_posts/` updates this list automatically.
  Home announcements and the News list show a **NEW** badge only on the latest
  published post in the current language. `_includes/news-new-badge.html` uses
  the publication-date order and matches the selected post by URL. The badge
  moves to the next new post when the site is rebuilt, with no time-based expiry.
  It pulses three times, then stays still; reduced motion preferences disable
  the animation. NEW identifies the latest post, not a visitor's read status.
  The home page proceeds from research areas to Research Radar and the student invitation;
  KARI ground-test videos appear on the Research pages.
- Publications combine citations generated from `_data/orcid.yaml` and
  `_data/sources.yaml` with the curated historical records described below.

## Shared visual styles

`_styles/-theme.scss` defines the shared palette, heading sizes, card spacing,
metadata sizes, and control height for both languages and light/dark themes.
Content cards use 24px padding/gaps on desktop and 20px padding/16px gaps at
700px and below. Use `--card-title-size` for card headings and `--meta-size`
for dates and authors instead of defining slightly different sizes per page.

Use `SEARCH Lab` in running text. General introductions and recruitment copy
cover space mission design and technology demonstration from Earth orbit to
deep space. Keep the six application areas in the same order across both
languages, with constellation design under Earth-Orbit Mission Design.

In current Korean research copy, use `궤도·궤적`, `지구궤도`, `궤도해석`,
`궤도삽입`, and `우주임무 설계` consistently. Preserve official titles and
historical source wording. About, Research, and For Students describe research
linked to national R&D programs, with participation scope and responsibilities
determined by research topics and project schedules; keep this principle
consistent in both languages.

Primary actions use `.action-button`; arrow links use `.text-link`.
Page-specific styles retain layout rules and intentional emphasis, such as the
Contact recruitment heading and centered inquiry card. News and Research Radar
use the same title, card, and metadata hierarchy. Keep both languages aligned
when changing templates; the Radar introduction was intentionally removed.

## Publications and prior research outputs

The Korean and English Publications pages combine automatic citations with
`_data/legacy-publications.yaml`, imported from the principal investigator's
[previous publications page](https://sites.google.com/view/dr-space/publications).
This file preserves the original records before 2025, including work before
SEARCH Lab. `_data/discovered-publications.yaml` adds research outputs verified
through public indexes, publishers, scholarly societies, and institutions,
including 2025–2026 records through 2026-10-02.
The expanded review adds 46 records (45 conference contributions and one
magazine feature). `_data/ip-publications.yaml` adds 27 records from the
owner-provided `지식재산권현황_20260420.xlsx`: five patents, 14 software entries,
seven trademark source records, and one design. The repeated KPLO class-38
entry is displayed once, and the 2011 ambiguity-resolution patent is excluded
at the owner's request, giving 25 additional displayed entries from these
27 records. Four owner-reported accepted manuscripts are stored separately in
`_data/accepted-publications.yaml`. The combined list displays 161 outputs:
23 articles/features (19 published and four accepted, awaiting publication),
99 conference contributions, 12 patent entries,
20 software entries, and seven trademark/design entries (six trademarks and one design).
The subsequent document review updates 16 existing entries using 13 copyright
registration certificates and three patent application notices. It confirms
13 software registrations and three patent filings, corrects eight titles to
the official document wording, without creating additional entries.
The follow-up public search confirms eight further records: six KPLO trademarks,
one satellite design, and one software registration from 2010. All 20 software
entries now have registration numbers. The 2026 thermal-protection patent remains
unconfirmed in public records. The excluded 2011 patent's research history is
retained in the audit files. The design
is filed under its official title, `인공위성`, and its actual filing year, 2023.

- Edit the appropriate curated file to add or correct records. Keep the original
  `citation` and `source` for provenance; `details` contains the displayed venue,
  date, and identifiers. Record verified corrections with `note` and
  `verification_source`. Missing dates are left unspecified. Optional
  `details_en` supplies English display text without changing the source title.
- Use `category: journal`, `conference`, `patent`, `software`, or
  `intellectual-property` (with `subtype: trademark` or `design`). Patent `status`
  is `registered`, `application`, `mixed`, or `unknown`, based on verified
  bibliographic records; it does not track current legal validity. A registered patent stays one record
  with both its application and registration numbers. At the owner's request,
  the TTFF international patent displays only US grant `US10649091B2`, with
  `status: registered`, its 2020 grant date, and filing year 2017. The former
  EU/JP entries and original citation remain in the audit history. Patent years are filing years
  where known; verified grant dates are included in the details. The supplied
  IP inventory has no application or registration numbers/dates. Where later
  documents establish these fields, use `registration_year` or `application_year`
  as the `year_basis` and update the displayed details. Otherwise, internal
  reference years use `year_basis: internal_reference_year`, explicit display
  labels, and `status: unknown`. Internal receipt references
  must never populate `application_number` or `registration_number`.
- Professional magazine contributions use `category: journal` and
  `subtype: magazine`; both language pages label them as magazine features.
- Accepted manuscripts use `category: journal`, `status: accepted`, and
  `accepted_date`. They appear above published articles, ordered by acceptance
  date, and do not receive a publication `date`, `year`, DOI, volume, or pages
  before those details are available. Titles, authors, and acceptance dates
  follow the owner's supplied information; `journal_source` verifies the venue
  name only. Once publication is confirmed, update the same record with the
  publication metadata and change `status` to `published`; do not add a duplicate.
- `_plugins/publications.rb` merges automatic citations by DOI or matching title
  and year, preserving curated details. The stored `_data/citations.yaml` remains
  generated data; do not edit it directly. ORCID refreshes preserve work categories
  for conferences, patents, and software.
- Both languages share these records and retain publication titles in their source
  language, with verified bibliographic corrections documented in the audit.
  Search covers titles, authors, details, and Korean/English author aliases.
- `_data/ip-publication-audit.yaml` maps all 43 inventory rows to the displayed
  entries and records title variations, duplicate decisions, missing identifiers,
  and current counts. Sixteen rows reconcile to 14 existing entries, including
  three overseas inventory rows historically linked at the patent-family level;
  that entry now displays only the US grant. The internal references are not
  assigned individually to the US application. Existing verified
  titles and identifiers take precedence over internal report titles; mappings
  without a shared official identifier remain documented inferences.
  The two KPLO class-38 trademark rows have the same title, class, and year.
  They are displayed as one entry with both internal references. The complete
  row-27 contributor list is used for display; row 26 remains in the source with
  `exclude: true` and `duplicate_of: ip-2022-3-0008`. This display decision does
  not establish that the two references denote the same legal right. Financial,
  department, and account columns are not imported; the workbook is not copied
  into the website.
- `_data/ip-document-audit.yaml` records the follow-up document verification,
  including file hashes, evidence pages, official names, and dates. Registration
  dates come from the certificate's registration field, not its creation,
  publication, or issue date. Patent filing dates come from the application-number
  notice. Keep prior internal titles in `title_aliases` and `search`, and retain
  the original inventory `citation` and `source`.
- `_data/ip-search-audit.yaml` records the later public search of all ten displayed
  entries with unverified filing/registration information. It preserves official
  KIPRIS and CROS evidence, search coverage, rejected matches, and remaining
  uncertainties. The KPLO class-38 entry links to registration `40-1883051` and
  remains a single displayed record. Direct correspondence between the two internal
  receipt references is still not documented. Trademark contributor names are
  distinct from KARI as the registered owner; the design's 25 creators match the
  official record in name and order.
- The software certificates name Korea Aerospace Research Institute as the
  corporate author. `copyright_author` records that role; `authors` retains
  the inventory's individual contributors and `contributor_role` labels them
  accordingly on the page. Patent `applicant` and `inventors` are separate.
  Original PDFs, addresses, identification numbers, and document access codes
  are not copied to the site.

### DOI and author ORCID verification

The original audit covers all 87 imported records and their 94 written author-name
variants (63 identity groups). One article was excluded at the owner's request
because the publisher's author list does not include the principal investigator.
The original collection therefore contributes 86 displayed records. The expanded
2026-10-02 search also verified a KoreaScience DOI absent from Crossref, bringing
the displayed DOI count to 12. The public-search snapshot and author results
are recorded in `_data/publication-discovery-audit.yaml`; the later inventory
import and updated output counts are in `_data/ip-publication-audit.yaml`.

- `_data/publication-audit.yaml` records each work's DOI result, evidence URLs,
  metadata discrepancies, author references, and inclusion decision.
- `_data/publication-discovery-audit.yaml` records additional works, per-source
  search coverage, duplicate and identity decisions, patent updates, and
  unresolved software candidates. DBpia and RISS query results were inspected
  through their final pages and checked against official proceedings. Public
  indexes and accessible sources cannot establish completeness for every
  database, private output, or unpublished patent application.
- `_data/author-identifiers.yaml` stores exact author-name aliases and the public
  evidence used to establish identity. Only `status: verified` entries produce
  ORCID links. Do not attach an iD based only on a matching name.
- Store a verified DOI in both `doi` and `id: doi:…`, with a resolving DOI `link`.
  Patent and software registration numbers remain separate fields. A missing DOI
  or unconfirmed ORCID means it was not established from the checked public
  sources; it does not mean the identifier cannot exist.
- Keep excluded curated records with `exclude: true` and `exclusion_reason`.
  The merge also blocks matching automatic citations from reintroducing them.
- Author ORCID links identify people; they do not assert that each work appears
  on their ORCID profile. The audit separately records matches against the PI's
  public ORCID works. This repository does not write to anyone's ORCID account.
- Preserve original `citation` text when correcting displayed metadata. Add the
  evidence to the audit and update `checked_on` when verifying it again.

Publications also has a daily public-source refresh for Crossref records, supported
KSAS/SASE programs, public patent metadata, and CROS software registrations.
Verified new records and metadata patches are stored in `_data/auto-publications.yaml`;
uncertain identity/participation stays in the workflow review artifact, outside the website.
See [`_publications/README.md`](_publications/README.md) for exact coverage, limitations,
the 09:37 KST schedule, and local validation. This is separate from Research Radar.

## Research Radar

The home page shows six recent papers; `/radar/` and `/en/radar/` show up to
12 papers per journal from **Journal of Guidance, Control, and Dynamics (JGCD)**,
**Journal of Spacecraft and Rockets (JSR)**, and **Acta Astronautica**.
These external papers are separate
from the lab's Publications records. Titles, authors, publication dates, topic
labels, and DOI links come from a cached Crossref snapshot; visitors do not need
an API key or a live request to the publisher.

- `_data/radar-settings.json` configures journal ISSNs, a 90-day publication
  window, topic keywords, and per-journal limits. Titles and available abstracts
  are used to match topics; abstracts and full text are not stored or displayed.
  Matching indicates subject relevance, not a ranking of paper quality.
- `_data/research-radar.json` is generated by `_radar/update.py`; do not edit it
  directly. Online publication dates take precedence over print dates. Missing
  days/months are left unspecified, and future or undated records are omitted.
- `_data/radar-curation.json` holds manually chosen `pinned` papers and
  `excluded_dois`. Pins appear in a separate **Lab-selected papers** group, in
  the configured order, and are not repeated in the recent-paper list. The
  initial list has no pins. Pins may be older than 90 days or outside the topic
  filter, but must resolve to research articles in a configured journal.
  Exclusions take precedence over pins.
- `_data/radar-ui.yaml`, `_includes/research-radar.html`,
  `_includes/radar-entry.html`, and `_styles/radar.scss` provide the bilingual UI.

For example, to pin a verified paper with an optional editorial note:

```json
{
  "pinned": [
    {
      "doi": "10.2514/1.g009818",
      "note": {
        "ko": "추천 이유를 작성하세요.",
        "en": "Add a short reason for selecting this paper."
      }
    }
  ],
  "excluded_dois": []
}
```

After changing settings or curation, regenerate the snapshot and check it:

```bash
python3 -m unittest discover -s _radar -p 'test_*.py'
python3 _radar/update.py
```

The script uses Python 3.11+ and `curl` with certificate verification enabled.
If one journal fails, its last successful list and collection timestamp remain
available with an update-delay notice. If all journals fail, the script exits without
replacing the snapshot. API retries are bounded, and output is written atomically.

Once pushed to `main`, `.github/workflows/update-research-radar.yaml` refreshes
the snapshot at approximately **10:17 and 22:17 KST** each day. GitHub can delay
scheduled jobs. To refresh on demand, run **update-research-radar** from Actions.
The workflow tests the processor, commits the new snapshot, and explicitly calls
the existing site-build workflow, because a `GITHUB_TOKEN` commit does not trigger
another push workflow. Live deployments share a concurrency group.

## Local development

Ruby version is pinned in `.ruby-version` (Ruby 3.4.10). GitHub Actions reads the same file.

```bash
bundle install
bundle exec jekyll serve
```

The site is served at <http://127.0.0.1:4000/>.

### Note for macOS 26 with Xcode 27

The Xcode 27 SDK declares macOS 27 APIs (e.g. `pipe2`) that do not exist on macOS 26,
so C extensions built against it can crash at runtime.
Build native gems against the macOS 26 SDK from the Command Line Tools:

```bash
SDKROOT=/Library/Developer/CommandLineTools/SDKs/MacOSX26.5.sdk bundle install
```
