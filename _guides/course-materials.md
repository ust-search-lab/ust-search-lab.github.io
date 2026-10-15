# 수업자료 게시 가이드

수업자료 목록은 한국어 `/students/courses/`, 영어 `/en/students/courses/`에 표시됩니다. `For Students`에서 이 목록으로 이동할 수 있으며, 과목별 강의계획서·강의노트·참고문헌·과제를 게시합니다.

AI 코딩 가이드는 연구실에 들어온 학생들이 공통으로 사용하는 안내자료로, 기존 `For Students`에 둡니다. 교과목 수업자료와는 별도로 운영합니다.

관리자는 `/admin/`의 **자료 관리 → 과목·학기별 수업자료**에서 파일과 과목 정보를 등록할 수 있습니다. 최초 GitHub 로그인 연결은 [CMS 설정 가이드](cms-setup.md)를 따르세요. CMS에 등록한 파일은 `downloads/materials/`에 저장되고, 과목 데이터로 한·영 페이지가 자동 생성됩니다. 아래는 저장소에서 직접 편집할 때의 방법입니다.

처음에는 `_data/courses.yaml`이 `courses: []`인 상태로 시작합니다. 실제 개설 정보와 자료가 준비되면 과목·학기별 항목을 추가하세요. 아래의 **예시 과목은 작성 방법 설명용이며 실제 개설 과목이 아닙니다.** 이 가이드가 있는 `_guides` 디렉터리는 사이트 빌드에서 제외됩니다.

## 1. 자료 파일 추가

과목과 학기를 구분하는 고유 ID를 정하고 자료를 다음과 같이 저장합니다. 같은 과목이라도 학기가 다르면 새 ID를 사용합니다.

```text
downloads/courses/sample-course-2027-spring/
├── syllabus.pdf
├── week-01-ko.pdf
└── week-01-en.pdf
```

파일명은 공백 없는 영문·숫자·하이픈 조합을 권장합니다. 외부 저장소의 코드나 자료는 파일을 복사하지 않고 `https://...` 링크로 등록할 수도 있습니다.

## 2. 과목·학기와 주차별 자료 등록

`_data/courses.yaml`의 빈 `courses: []`를 아래와 같은 목록으로 바꿉니다. 이미 항목이 있다면 기존 `courses:` 아래에 같은 들여쓰기로 새 `- id:` 항목을 추가합니다. `courses:` 키를 중복해서 만들지 마세요.

```yaml
courses:
  - id: sample-course-2027-spring
    term_order: 202701
    term:
      ko: "2027년 봄학기"
      en: "Spring 2027"
    title:
      ko: "예시 과목"
      en: "Sample Course"
    description:
      ko: "수업자료 등록 방법을 보여 주는 예시입니다."
      en: "An example showing how to register course materials."
    updated: "2027-03-02"
    overview:
      - label:
          ko: "강의계획서"
          en: "Syllabus"
        url: "/downloads/courses/sample-course-2027-spring/syllabus.pdf"
        type: "PDF"
    weeks:
      - number: 1
        title:
          ko: "수업 소개"
          en: "Course Introduction"
        updated: "2027-03-02"
        materials:
          - label:
              ko: "1주차 강의자료"
              en: "Week 1 Lecture Notes"
            url:
              ko: "/downloads/courses/sample-course-2027-spring/week-01-ko.pdf"
              en: "/downloads/courses/sample-course-2027-spring/week-01-en.pdf"
            type: "PDF"
```

- `id`: 과목·학기마다 고유한 URL용 이름입니다. 영문 소문자·숫자·하이픈만 사용하고 게시 후에는 유지합니다.
- `term_order`: 최신 학기부터 정렬하기 위한 정수입니다. `YYYYNN` 형식으로, 예를 들어 `202701`은 2027년 첫 학기, `202702`는 그다음 학기로 사용합니다. `term`에는 학생에게 보여 줄 학기명을 따로 적습니다.
- `title`, `description`, `term`, 각 자료의 `label`, 주차의 `title`: `ko`와 `en`을 모두 작성합니다.
- `updated`: 과목 또는 해당 주차의 자료를 마지막으로 수정한 날짜입니다. YAML에서 문자열로 유지되도록 `"YYYY-MM-DD"` 형식으로 따옴표를 붙입니다.
- `overview`: 강의계획서 등 과목 공통자료 목록입니다. 공통자료가 없으면 이 항목을 생략할 수 있습니다.
- `weeks`: 주차별 목록입니다. `number`를 숫자로 쓰고, 표시할 순서대로 등록합니다. 아직 주차별 자료가 없다면 `weeks: []`로 둡니다.
- `url`: 두 언어가 같은 자료를 사용하면 문자열 하나로, 서로 다른 자료를 사용하면 예시처럼 `ko`와 `en`으로 나누어 적습니다. CMS에서는 이 한·영 객체 형식을 사용하며, `en`이 비어 있으면 영어 페이지도 `ko` 파일을 사용합니다. 사이트 내부 경로는 `/downloads/...`처럼 `/`로 시작하고, 외부 주소는 `https://...` 전체를 적습니다.
- `type`: 자료 옆에 표시할 형식입니다. `PDF`, `ZIP`, `Code` 등 학생이 알아보기 쉬운 값을 적습니다.

주차에 강의노트·참고논문·과제 안내를 여러 개 올리려면 `materials:` 아래에 `label`, `url`, `type`을 갖춘 항목을 더 추가합니다. 계산 코드나 실습자료는 해당 과목에 필요한 경우 같은 방식으로 등록합니다.

## 3. 한국어·영어 과목 페이지 자동 생성

`_plugins/materials.rb`가 각 과목의 `id`로 다음 두 페이지를 빌드할 때 자동 생성합니다. 별도의 페이지 파일은 만들 필요가 없습니다.

- `/students/courses/sample-course-2027-spring/`
- `/en/students/courses/sample-course-2027-spring/`

과목 레이아웃이 소개, 공통자료, 주차별 자료, 수정일과 상위 페이지 링크를 표시하며 언어 전환도 연결합니다. 과목을 데이터 목록에서 삭제하면 자동 생성 페이지도 다음 빌드에서 없어집니다.

더 긴 과목 안내가 필요하면 원하는 언어의 해당 경로에 `index.md`를 만들 수 있습니다. 예를 들어 한국어 파일은 다음과 같습니다. 이 경우 생성기는 기존 파일의 본문을 유지합니다.

```markdown
---
layout: course
title: "예시 과목"
ref: course-sample-course-2027-spring
parent_ref: students
course_id: sample-course-2027-spring
---

추가 안내 본문
```

수동 페이지가 있다면 과목을 삭제할 때 그 파일도 함께 삭제하세요. 날짜·고유 ID·주차 중복·누락된 로컬 파일·외부 링크 형식 오류는 빌드에서 검사합니다.

## 4. 기존 자료 업데이트

파일을 추가하거나 교체한 뒤 해당 자료의 `url`과 제목을 확인합니다. 새 주차를 게시할 때는 `weeks:`에 항목을 추가합니다. 주차 자료를 변경했다면 **그 주차와 과목 양쪽의 `updated`**를 실제 수정일로 바꿉니다. 강의계획서 등 공통자료만 변경했다면 과목의 `updated`를 바꿉니다. 날짜는 자동 갱신되지 않습니다.

자료를 삭제하거나 파일명을 변경할 때는 데이터에 남은 링크도 함께 수정합니다. 한국어·영어 자료가 별도로 있는 경우 두 언어의 경로와 페이지를 모두 확인합니다.

## 5. 확인하고 게시

저장소 루트에서 사이트를 빌드합니다.

```sh
bundle exec jekyll build
```

필요하면 `bundle exec jekyll serve`로 로컬 사이트를 열어 다음을 확인합니다.

- 한국어·영어 수업자료 목록에 새 과목이 올바른 학기 순서로 나타나는지
- 각 과목 페이지의 주차, 자료명, 수정일과 언어 전환이 맞는지
- 모든 PDF·ZIP·코드 링크가 실제 자료로 연결되는지

직접 편집할 때는 자료 파일과 `_data/courses.yaml`을 함께 Git으로 커밋하고 기존 게시 절차에 따라 푸시합니다. 수동으로 만든 과목 페이지가 있다면 함께 반영합니다. CMS에서 게시하면 저장소 반영과 이후 사이트 빌드·배포가 기존 GitHub Actions를 통해 진행됩니다.
