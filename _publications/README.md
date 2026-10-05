# Public research output updates

`update.py` supplements ORCID citations with public-source discovery and verified
metadata updates. It does not claim a complete inventory of all research outputs.
The owner selected **public sources only**; there are no institutional-system,
private-file, login, or API-key connections.

## Connected sources

| Source | Coverage | Automatic inclusion |
| --- | --- | --- |
| Crossref | DOI journal articles and conference papers; ORCID query, recent author/affiliation search, accepted-title checks | Matching ORCID, exact name plus KARI affiliation, or known title/DOI plus matching author |
| KSAS / SASE | Public proceedings linked by the society home/event pages and existing verified records, current year and prior two years | Explicit Park/KARI attribution and past session date |
| Google Patents | Public Korean/English inventor-and-assignee search, and existing patent publication pages | Exact inventor and KARI applicant; known application/registration numbers update existing records |
| CROS | Existing software registrations and up to 400 recent KARI search records, topic-filtered for discovery | Known registration number or exact known title plus corporate author; new corporate-only records require confirmation of lab participation |

Public conference programs establish a program listing, not actual attendance.
Crossref only covers deposited metadata. Society discovery only covers the two
connected sites and their supported public program format. AIAA and other
international conference papers are included when discoverable through Crossref.
DBpia's author-list login gate is not bypassed. Other societies, login-only indexes,
unpublished applications, and trademark/design discovery are **not connected**.
Google Patents is a public secondary index; grant documents/dates are bibliographic
facts and are not an opinion about current legal validity or ownership.

## Behavior

- Daily at approximately **09:37 KST**, `update-publications.yaml` tests and runs
  collection, saves the review report as a GitHub Actions artifact, commits changes
  to `_data/auto-publications.yaml`, and explicitly invokes site deployment.
- Until this workflow is pushed to `main`, only local runs occur.
- The original weekly ORCID workflow and Research Radar remain separate.
- The generated file contains new records and patches targeting curated `id` or
  `audit_key`. Curated titles, contributors, exclusions, and original provenance
  remain authoritative. Accepted papers can advance to published; applications can
  advance to registered. Missing dates stay missing, and grants never downgrade.
- A conference contribution and subsequent journal article remain distinct.
  Patent jurisdictions and corporate software authorship remain distinct.
- Failed sources retain prior data. A wholly failed run writes no output. Partial
  Crossref queries are reported explicitly. Remote empty/missing results never
  delete existing publications. Results are bounded, so successful collection is
  not a completeness claim.
- Only bibliographic fields are retained. CROS IDs, addresses, full registration
  responses, abstracts, claims, full papers, and access codes are not published.
- `_publications/review.json` is gitignored and excluded from Jekyll. The workflow
  summary lists coverage; `publication-review` artifacts retain candidates for 30
  days. Public visitors see only the confirmed publication records.

## Running and reviewing

```sh
python -m pip install -r _publications/requirements.txt
python -m unittest discover -s _publications -p 'test_*.py'
bundle exec ruby _publications/test_merge.rb
python _publications/update.py
bundle exec jekyll build
```

Use `--output-dir /path/to/preview` for a non-publishing trial. It still reads the
current repository's settings and previous snapshot. Review candidates and source
failures in the JSON report. To exclude a candidate, put its `_source_id` in
`excluded_source_ids` in `_data/publication-automation.json`. Only after confirming
participation, add it to `approved_source_ids`, or add the fully attributed record
to the appropriate curated YAML file. Those are editorial decisions, not an API
authentication requirement. New software contributors should be recorded in the
curated file with the appropriate `contributor_role`.

Source interfaces are public and can change. When a parser fails, update it against
the actual public response and add a regression test; never silently bypass a login
or assume an empty response means all previous records should be removed.

References: [Crossref REST API](https://www.crossref.org/documentation/retrieve-metadata/rest-api/),
[KSAS](https://ksas.or.kr/), [SASE](https://sase.or.kr/main/),
[Google Patents](https://patents.google.com/), [CROS](https://www.cros.or.kr/).
