# Decap CMS 최초 연결과 자료실 운영

이 사이트는 Jekyll과 GitHub Pages 배포를 그대로 사용하고, `/admin/`의 Decap CMS로 공개 자료를 편집합니다. GitHub 로그인의 인증 코드 교환만 Cloudflare Workers에서 처리합니다.

현재 관리자 화면·자료실과 GitHub OAuth 인증 Worker가 연결되어 있습니다. `/admin/`에서 **Login with GitHub**로 로그인하세요. 인증 서비스 상태는 [Worker의 `/health`](https://search-lab-cms-auth.jpark-275.workers.dev/health)에서 확인할 수 있습니다. 아래 최초 설정 절차는 인증 서비스를 다시 구성할 때 참고하세요. `_data/cms.yaml`의 인증 주소를 비우면 `/admin/`은 최초 설정 안내를 표시합니다.

## 일상적인 자료 관리

집이나 출장지 등 어디서든 브라우저로 [관리자 화면](https://ust-search-lab.github.io/admin/)에 접속하여 GitHub로 로그인하면 됩니다. 개인 컴퓨터를 켜 두거나 Git 명령을 실행할 필요가 없습니다. 사이트 저장소에 쓰기 권한이 있는 계정으로 일반 자료와 수업자료를 모두 관리합니다.

- **자료 관리 → 일반 자료:** 연구 참고자료, 발표자료, 공통 학습자료와 예제 코드를 등록합니다.
- **자료 관리 → 수업자료:** 과목·학기별 강의계획서와 주차별 강의노트·과제를 등록합니다.
- 방문자는 **Resources** 한 페이지에서 두 목록을 볼 수 있습니다. **For Students**도 이 페이지의 수업자료 목록으로 연결됩니다. 같은 자료를 두 목록에 중복 등록할 필요가 없습니다.
- 파일은 한 번 업로드하고 다른 과목에서도 필요하면 기존 파일을 선택하거나 같은 링크를 사용합니다. 큰 파일·영상은 외부 저장소의 HTTPS 링크로 연결합니다.

게시 후 자동 배포가 완료되면 사이트에 반영됩니다. 아래 4~5절에서 각 등록 항목을 확인할 수 있습니다.

## 1. Cloudflare 계정과 인증 Worker 만들기

1. [Cloudflare](https://dash.cloudflare.com/sign-up) 계정을 만듭니다. 홈페이지는 GitHub Pages에 계속 두며, 별도 도메인을 구입할 필요는 없습니다.
2. Node.js 22 이상이 설치된 터미널에서 저장소의 `_cms/oauth/` 폴더로 이동합니다.
3. 다음 명령으로 Cloudflare 계정에 로그인하고 Worker를 배포합니다.

```sh
cd _cms/oauth
npx wrangler@4.151.0 login
npx wrangler@4.151.0 deploy
```

배포 결과의 `https://search-lab-cms-auth.<계정별이름>.workers.dev` 주소를 기록하세요. 아직 GitHub 인증 설정이 없으므로 `/health` 접속 시 설정이 완료되지 않았다는 메시지가 나오는 것이 정상입니다.

## 2. GitHub OAuth App 등록

사이트를 관리할 GitHub 계정 또는 조직의 **Settings → Developer settings → OAuth Apps → New OAuth App**에서 다음과 같이 등록합니다.

| 항목 | 값 |
|---|---|
| Application name | SEARCH Lab Content Manager |
| Homepage URL | `https://ust-search-lab.github.io/admin/` |
| Authorization callback URL | 위 Worker 주소 뒤에 `/callback`을 붙인 주소 |

등록 후 **Client ID**를 확인하고 **Generate a new client secret**으로 비밀키를 발급합니다. 아래 명령을 실행하면 값을 입력하는 프롬프트가 나옵니다. 각각 해당 값을 입력하세요.

```sh
npx wrangler@4.151.0 secret put GITHUB_CLIENT_ID
npx wrangler@4.151.0 secret put GITHUB_CLIENT_SECRET
```

Client Secret은 Cloudflare의 Secret으로만 저장하세요. GitHub 저장소나 채팅에 붙여 넣지 않습니다. 두 값이 등록되면 Worker의 `/health`에서 `OAuth service ready`를 확인할 수 있습니다.

이 Worker는 공개 저장소 편집에 필요한 `public_repo` 권한을 요청합니다. 로그인한 사용자가 이 사이트 저장소에 쓰기 권한이 있는지도 확인합니다. GitHub 조직이 OAuth 앱 승인을 제한하는 경우 조직 소유자의 앱 승인이 추가로 필요합니다.

## 3. 사이트에 인증 주소 등록

저장소의 `_data/cms.yaml`을 다음처럼 수정합니다. 실제 Worker 주소를 사용하고 `/callback`이나 끝의 `/`는 붙이지 마세요.

```yaml
auth_base_url: "https://search-lab-cms-auth.YOUR-SUBDOMAIN.workers.dev"
```

이 변경과 이번에 추가한 CMS 파일들을 기존 게시 절차대로 GitHub `main`에 반영합니다. 배포가 완료되면 `https://ust-search-lab.github.io/admin/`에서 **Login with GitHub**를 누릅니다. 해당 저장소의 쓰기 권한이 있는 계정으로 승인하세요.

관리자 화면을 로컬·배포 미리보기에서 열더라도 저장 대상은 설정된 GitHub `main`입니다. 실제 게시 확인은 정식 사이트에서 진행하세요. 인증 Worker는 정식 사이트의 출처만 허용합니다.

## 4. 일반 자료 등록

관리자 화면에서 **자료 관리 → 일반 자료**를 엽니다.

1. 자료 목록에 새 항목을 추가합니다.
2. 고유 ID, 한·영 제목과 설명, 분류, 수정일을 입력합니다.
3. 파일을 업로드하거나 **Insert from URL**로 외부 HTTPS 링크를 입력합니다.
4. 영어판 파일이 따로 있으면 추가하고, 같은 파일이면 비워 둡니다.
5. 파일 형식에 `PDF`, `ZIP`, `Code`, `Link` 등을 적고 게시합니다.

파일은 `downloads/materials/`, 목록은 `_data/library.yaml`에 저장됩니다. 관리자가 Git 명령을 실행할 필요는 없습니다. 게시 후 기존 GitHub Actions가 빌드·배포하므로 사이트 반영까지 잠시 기다려 주세요. GitHub의 Actions 화면에서 완료 여부를 확인할 수 있습니다.

한국어 `/resources/#general`과 영어 `/en/resources/#general`에서 제목·설명 검색, 분류 필터, 최근 수정일순 목록을 제공합니다. 분류는 공통 학습자료·연구자료·코드·실습이며, 특정 과목의 강의노트·과제는 수업자료에 등록합니다. 영어판 파일이 없으면 공통 파일을 사용합니다. 실제 자료가 없는 동안에는 빈 목록 안내가 표시됩니다.

자료 입력 폼의 파일 선택기에서는 업로드를 파일당 20 MiB로 제한했습니다. 큰 파일은 외부 저장소에 올린 뒤 HTTPS 링크를 입력하세요. 파일명은 공백 없는 영문·숫자·하이픈 조합을 권장합니다. 별도의 미디어 목록에서 직접 업로드할 때는 이 폼의 용량 제한이 적용되지 않으므로 같은 기준을 지키세요. 미디어 목록에서 기존 파일을 삭제할 때는 해당 파일을 사용하는 다른 자료와 과목이 없는지 확인하세요.

이 자료실은 공개 배포용입니다. CMS의 GitHub 로그인은 편집자 인증이며, 게시된 파일은 방문자 누구나 받을 수 있습니다. 비공개 자료를 공개 저장소에 올리지 마세요.

## 5. 수업자료 관리

**자료 관리 → 수업자료**에서 과목, 학기, 강의계획서, 주차별 자료를 추가합니다. 각 과목의 고유 ID는 예를 들어 `orbital-mechanics-2027-spring`처럼 정합니다. 한·영 제목·설명·학기명을 입력하면 사이트 빌드 시 두 언어의 과목 상세 페이지가 자동으로 만들어지고, Resources의 수업자료 목록에 표시됩니다.

각 자료의 **공통·한국어** 파일을 지정하고, 필요한 경우 영어판을 추가하세요. 영어판을 비워 두면 영어 페이지에서도 공통 파일을 사용합니다. 기존의 문자열 URL과 한·영 URL 데이터 형식도 계속 지원합니다.

과목을 게시한 뒤에는 고유 ID를 유지하세요. ID는 과목 URL을 결정합니다. 주차 자료를 수정할 때는 해당 주차와 과목의 수정일을 함께 바꿉니다. 자세한 데이터 형식은 [수업자료 게시 가이드](course-materials.md)를 참고하세요.

## 6. 유지 관리와 확인

외부 서비스를 연결하기 전에도 다음 명령으로 검증할 수 있습니다.

```sh
bundle exec ruby _cms/test_materials.rb
node --test _cms/oauth/worker.test.mjs
bundle exec jekyll build
```

로그인 연결 후에는 다음을 실제 계정으로 확인하세요.

- 저장소 쓰기 권한이 있는 관리자 로그인과 로그아웃
- 쓰기 권한이 없는 계정의 접근 거부
- 첫 자료 등록 → Actions 배포 완료 → 한·영 페이지와 파일 링크 확인
- 새 과목 등록 → 한·영 상세 페이지와 언어 전환 확인

연결 문제는 먼저 Worker의 `/health`, GitHub OAuth App의 callback 주소, `_data/cms.yaml`의 Worker 주소, 팝업 허용 여부와 GitHub 조직의 앱 승인을 확인하세요. 사이트 주소를 변경하면 Worker의 `SITE_ORIGIN`, CMS의 사이트 주소와 OAuth App 설정도 함께 변경합니다.

Decap은 CDN의 `3.17.1` 버전으로 고정되어 있습니다. 버전을 변경할 때는 관리자 화면과 실제 게시 흐름을 다시 확인하세요. 인증 Worker 코드와 테스트는 `_cms/oauth/`에 있으며, 이 폴더와 `_guides/`는 공개 사이트 빌드에서 제외됩니다.

참고: [Decap GitHub 연동](https://decapcms.org/docs/github-backend/), [수동 초기화](https://decapcms.org/docs/manual-initialization/), [GitHub OAuth](https://docs.github.com/en/apps/oauth-apps/building-oauth-apps/authorizing-oauth-apps), [Cloudflare Workers Secrets](https://developers.cloudflare.com/workers/configuration/secrets/).
