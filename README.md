![on-push](../../actions/workflows/on-push.yaml/badge.svg)
![on-pull-request](../../actions/workflows/on-pull-request.yaml/badge.svg)
![on-schedule](../../actions/workflows/on-schedule.yaml/badge.svg)

# SEARCH Lab Website

Official website of SEARCH Lab (Space Exploration ARCHitecture Laboratory) at UST.

Visit **[ust-search-lab.github.io](https://ust-search-lab.github.io/)**

_Built with [Lab Website Template](https://greene-lab.gitbook.io/lab-website-template-docs) v1.4.0_

## Site structure (Korean / English)

- Korean pages live at the root (`/`, `/about/`, ...) and English pages under `/en/` (`/en/`, `/en/about/`, ...).
  The language comes from the `lang` front matter (default `ko`, `en` for everything under `en/`).
- Each page and member profile has a `ref` key. The language switch in the header links to the page with the same `ref` in the other language.
- Member profiles are in `_members/`, one file per language (`name.md` with `lang: ko`, `name-en.md` with `lang: en`).
- Interface text for both languages is in `_data/i18n.yaml`.
- Publications are generated from the ORCID iD in `_data/orcid.yaml` (plus any entries in `_data/sources.yaml`).

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
