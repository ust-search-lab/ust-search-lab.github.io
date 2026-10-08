# Public research output updates

`update.py` discovers and updates public research-output metadata for the PI and
collaborating researchers. It does not claim a complete inventory. The owner
selected **public sources only**: no institutional-system, private-file, login,
or API-key connections are used.

## Attribution and page scope

`_data/publication-automation.json` contains a `researchers` array. Stable IDs are
`jae-ik-park`, `seung-ryeol-oh`, and `jungju-bae`; each identity has verified name
aliases, historical affiliations, an internal ORCID, and a `main_publications`
flag. These collection identifiers do not add ORCID buttons to People pages.

Confirmed records carry `researcher_ids`. The main Publications view contains
PI-participating outputs; personal profile views contain that person's verified
career outputs, including work at earlier institutions. Shared works are stored
once and can appear in several views. Matching DOIs, same-country patent
application/registration numbers, and software registration numbers prevent
duplicate records. Participant IDs are unioned on both records and curated-target
patches. Authors, inventors, corporate owners, and individual software contributors
remain different roles.

Curated records include `_data/collaborator-publications-oh.yaml` and
`_data/collaborator-publications-bae.yaml`. Existing curated participant names are
matched only against full aliases. The former PI-only automatic snapshot is
migrated once to inherit curated participant IDs, preserving historical PI
software attribution. Newly discovered automatic records require explicit
verified participant IDs. A matching work title never establishes an additional
researcher's participation.

There is a documented KAIST namesake of Seungryeol Oh in an unrelated field.
Consequently `allow_affiliation_match: false` is set for both collaborators:
Crossref name plus university/institute alone remains a review candidate. A
matching author ORCID, a public self-DOI on the confirmed ORCID record plus an
exact author alias, or previously curated participation is required. A conflicting
author ORCID always prevents attribution, including ORCID-linked DOI discovery.
Corrections, errata, and retraction notices are held for review rather than
automatically counted as ordinary journal articles.
New collaborator patent inventor/assignee matches also require review unless
participation in the same application is already curated.

## Connected sources

| Source | Coverage | Automatic inclusion |
| --- | --- | --- |
| ORCID public works + Crossref | Full-career public journal/conference self-DOIs on each configured ORCID record | Crossref supplies complete metadata and a matching author alias/ORCID; non-DOI and unsupported works require manual source verification |
| Crossref | DOI journals/conferences; ORCID query, recent author-alias searches, accepted/under-review title checks | Matching author ORCID or known participant; legacy PI also allows exact full name plus known affiliation |
| KSAS / SASE | Public proceedings linked by society home/event pages and existing verified records; current year and prior two years | Exact Korean author name with a configured historical institution and a past session date |
| Google Patents | Public inventor-alias searches and existing verified patent pages | Legacy PI name plus configured applicant; collaborators require curated participation or reviewed attribution; same-country application numbers track grants |
| CROS | Existing software registrations and up to 400 recent KARI search records, topic-filtered | Existing verified registration/title and corporate owner can update metadata; new corporate-only records require verified individual participation |

Public programs verify a conference listing, not actual attendance. ORCID only
exposes public works; Crossref only covers deposited metadata. Only the two
societies' supported public program format is connected. AIAA and other
international conference papers can be found through Crossref. DBpia's author-list
login gate is not bypassed. Unpublished applications, login-only indexes, other
society formats, and trademark/design discovery are not connected. Google Patents
is a public secondary index: grant facts do not establish current legal validity.

## Behavior

- At approximately **09:37 KST daily**, the workflow tests collection, refreshes
  metadata, uploads a review artifact, commits `_data/auto-publications.yaml`, and
  invokes site deployment when records change. The original weekly PI ORCID
  citation workflow and Research Radar remain separate.
- Each researcher/source pair receives a reserved share of the total request
  budget. A prolific first researcher or unavailable source cannot consume later
  researchers' reserved requests. Unused earlier requests roll forward, so the
  final software collector can use the remaining overall budget. Responses are
  cached across the entire run.
  Source/person coverage and request usage are included in the review report.
- Generated records patch curated `id` or `audit_key` values. Curated titles,
  contributors, exclusions, and original provenance stay authoritative. Accepted
  and under-review papers can advance to published; patent applications can
  advance to registered. Missing dates stay absent and grants never downgrade.
- A conference paper and later journal article remain distinct. Patent
  jurisdictions remain distinct; an application and its later grant in the same
  jurisdiction represent one output. Same-title conference records with different
  explicit proceedings events or conflicting session dates remain distinct.
- Source errors preserve prior records. A wholly failed run leaves the previous
  publication file untouched and writes an error report. Empty/missing remote
  results do not delete publications. Bounded result sets, unsupported ORCID
  works, query failures, and exhausted budgets are reported rather than treated
  as proof of completeness.
- Only bibliographic fields are retained. CROS internal IDs, addresses, full
  registration responses, abstracts, claims, papers, and access codes are not
  published. `_publications/review.json` is gitignored/excluded from Jekyll;
  `publication-review` artifacts retain candidates for 30 days.

## Running and reviewing

```sh
python -m pip install -r _publications/requirements.txt
python -m unittest discover -s _publications -p 'test_*.py'
bundle exec ruby _publications/test_merge.rb
python _publications/update.py
bundle exec jekyll build
```

For a historical backfill or a focused trial:

```sh
python _publications/update.py --backfill --output-dir /tmp/publications-preview
python _publications/update.py --researcher seung-ryeol-oh --source orcid --source crossref --output-dir /tmp/oh-preview
```

`--researcher` and `--source` may repeat. A trial still reads the current repository
settings and prior snapshot; other researchers' existing records are preserved.
`--backfill` expands the author-search/program year window to the configured
`backfill_start_year` (1990). It does not invent old proceedings URLs or remove
request/result limits. ORCID self-DOIs are read across the whole career on every
run, so a newly added older work is still discovered. Use curated, source-verified
records to supplement unsupported historical proceedings, non-DOI works, and
bounded search results. GitHub Actions manual dispatch also offers `backfill`.

To exclude a candidate, add its `_source_id` to `excluded_source_ids` or add a
curated record with `exclude: true`. After verifying a candidate's individual
participation, add it to `approved_source_ids`, or add a fully attributed curated
record with `researcher_ids` and verification sources. An institution-only
software record cannot be approved without individual participant IDs; record
verified contributors in curated data with the appropriate `contributor_role`.
Approvals are editorial decisions, not API authentication.

Public interfaces can change. Parser failures require inspection of the actual
public response and a regression test. Do not bypass authentication or interpret
an empty response as removal of all historical records.

References: [ORCID public record API](https://info.orcid.org/documentation/api-tutorials/api-tutorial-read-data-on-a-record/),
[Crossref REST API](https://www.crossref.org/documentation/retrieve-metadata/rest-api/),
[KSAS](https://ksas.or.kr/), [SASE](https://sase.or.kr/main/),
[Google Patents](https://patents.google.com/), [CROS](https://www.cros.or.kr/).
