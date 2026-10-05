---
title: AI Coding Guide
ref: ai-coding-guide
parent_ref: students
description: 맥·리눅스·윈도에서 AI 코딩 환경을 구성하고, Python 궤도 계산을 구현·검증·기록하는 SEARCH Lab 학생용 따라하기 가이드입니다.
---

<p class="guide-breadcrumb"><a href="{{ '/students/' | relative_url }}">For Students</a> <span aria-hidden="true">/</span> 실습 가이드</p>

# 학생 연구자를 위한 AI 코딩 가이드
{: .page-title }

맥·리눅스·윈도에서 개발 환경을 만들고, AI와 함께 간단한 궤도 계산 프로그램을 작성합니다. 코드 실행, 결과 검증, 변경 이력 저장까지 한 번에 따라 해보세요.
{: .page-intro }

<div class="guide-meta"><span>입문 · Python 실습</span><span>예상 60–90분 · 설치 시간 별도</span><span>문서 확인 2026.10.05</span></div>
<div class="guide-actions">
  <a class="guide-button" href="#setup">내 운영체제로 시작하기 <span aria-hidden="true">↓</span></a>
  <a class="guide-button guide-button-secondary" href="{{ '/downloads/search-lab-ai-coding-starter.zip' | relative_url }}" download>참고 코드 ZIP</a>
  <button class="guide-button guide-button-secondary" type="button" data-guide-print hidden>인쇄 · PDF로 저장</button>
</div>

<nav class="guide-toc" aria-label="가이드 목차" markdown="1">
1. [준비물과 진행 순서](#start)
2. [운영체제별 설치](#setup)
3. [Python 프로젝트 만들기](#project)
4. [AI 코딩 도구 연결](#assistant)
5. [첫 실습: 원궤도 계산](#exercise)
6. [검증하고 확장하기](#verify)
7. [Git 저장과 재현](#share)
8. [자주 만나는 문제](#troubleshooting)
9. [공식 문서 모음](#references)
</nav>

{% include section.html %}

## 01. 준비물과 진행 순서
{: #start }

이 문서에서 **바이브 코딩**은 원하는 작업을 자연어로 설명하며 AI와 코드를 만드는 실습을 뜻합니다. 연구에 활용하려면 계산의 가정과 단위를 이해하고 결과를 직접 검증하는 과정까지 익혀야 합니다.

| 구성 | 역할 | 이 가이드의 선택 |
|---|---|---|
| 편집기 | 파일을 열고 수정하는 작업 공간 | VS Code 또는 Cursor |
| Git | 변경 이력과 돌아갈 지점 저장 | 모든 운영체제에서 사용 |
| Python + uv | 계산 실행, 프로젝트별 Python 환경 관리 | Python 3.12 계열로 실습 |
| AI 코딩 도구 | 코드 설명·작성·수정 지원 | Codex, Claude Code, Copilot, Cursor 중 하나 |

**처음이라면 VS Code + Git + uv를 설치하고, 사용 가능한 계정에 맞춰 AI 도구 하나를 선택하세요.** Cursor를 선택하면 편집기로 Cursor를 사용해도 됩니다. 아래의 파일 만들기·터미널 실습은 두 편집기에서 같은 방식으로 진행할 수 있습니다.

GitHub 계정은 마지막 온라인 공유 단계에서만 필요합니다. AI 기능의 이용 가능 여부·사용량·비용은 선택한 서비스와 계정에 따라 달라지므로 로그인 화면에서 확인합니다. 기본 Python 실습에는 Node.js, Docker, GPU가 필요하지 않습니다.

명령어는 **터미널**에, AI에게 할 요청은 **AI 채팅창**에 입력합니다. 코드 블록은 위에서부터 한 줄씩 실행하고, 오류가 나면 그 줄에서 해결한 뒤 진행하세요. 이 실습에는 공개된 수치와 자체 작성한 예제만 사용합니다.

{% include section.html %}

## 02. 내 운영체제에 맞게 설치하기
{: #setup }

아래에서 **하나만** 선택합니다. 맥은 Terminal, 리눅스는 터미널, 윈도 기본 경로는 PowerShell을 사용합니다. 이미 설치한 도구는 버전을 확인하고 건너뛰어도 됩니다.

<div class="guide-os-links">
  <a href="#macos">macOS <span>맥</span></a>
  <a href="#linux">Linux <span>Ubuntu · Debian · Fedora</span></a>
  <a href="#windows">Windows <span>PowerShell</span></a>
</div>

<details class="guide-os" id="macos" markdown="1">
<summary>macOS · 맥에서 설치</summary>

### 2A-1. 편집기 설치

1. [VS Code 다운로드](https://code.visualstudio.com/download)에서 맥용을 선택합니다. Apple Silicon(M 계열)과 Intel 중 자신의 기기에 맞는 버전을 고릅니다.
2. 다운로드한 앱을 **응용 프로그램(Applications)** 폴더로 옮겨 실행합니다.
3. `Cmd+Shift+P`로 명령 팔레트를 열고 **Shell Command: Install 'code' command in PATH**를 실행합니다. 이후 터미널을 새로 엽니다.

Cursor를 사용할 경우 [Cursor 빠른 시작](https://cursor.com/docs/get-started/quickstart)에 따라 설치합니다. 이후 `code .` 대신 Cursor의 **File → Open Folder**로 실습 폴더를 열면 됩니다.

### 2A-2. Git 설치

Spotlight에서 **Terminal**을 검색해 실행하고 다음을 입력합니다.

```bash
git --version
```

버전이 표시되면 다음으로 넘어갑니다. 개발 도구 설치 창이 뜨면 설치를 마칩니다. Git이 없고 설치 창도 뜨지 않는 경우 다음을 실행합니다.

```bash
xcode-select --install
```

이미 Homebrew를 사용한다면 `brew install git`도 가능합니다. 두 방법을 모두 사용할 필요는 없습니다. [Git 맥 설치](https://git-scm.com/install/mac) · [Homebrew 안내](https://brew.sh/ko/)

### 2A-3. uv 설치와 확인

아래는 uv 공식 설치 스크립트를 받아 실행하는 명령입니다.

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

터미널을 완전히 닫았다가 다시 열고 확인합니다.

```bash
git --version
uv --version
code --version
```

**완료 기준:** Git·uv 버전이 출력되고 편집기가 열립니다. `code` 명령이 없어도 **File → Open Folder**로 진행할 수 있습니다. [VS Code 맥 설정](https://code.visualstudio.com/docs/setup/mac) · [uv 설치](https://docs.astral.sh/uv/getting-started/installation/)

[03. Python 프로젝트 만들기로 이동](#project)
</details>

<details class="guide-os" id="linux" markdown="1">
<summary>Linux · 리눅스에서 설치</summary>

### 2B-1. Git과 다운로드 도구 설치

Ubuntu·Debian에서는 다음을 실행합니다.

```bash
sudo apt update
sudo apt install git curl
```

Fedora에서는 다음을 실행합니다. 다른 배포판은 [Git 리눅스 설치](https://git-scm.com/install/linux)를 확인합니다.

```bash
sudo dnf install git curl
```

`sudo` 암호 입력 중에는 글자가 표시되지 않을 수 있습니다. 입력 후 Enter를 누릅니다.

### 2B-2. 편집기 설치

[VS Code 리눅스 설치](https://code.visualstudio.com/docs/setup/linux)에서 배포판과 CPU에 맞는 패키지를 받습니다. Ubuntu·Debian은 `.deb`, Fedora 계열은 `.rpm` 패키지를 소프트웨어 설치 앱으로 엽니다. Cursor를 선택했다면 [공식 Linux 설치 절차](https://cursor.com/docs/get-started/quickstart)를 사용합니다.

### 2B-3. uv 설치와 확인

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

새 터미널에서 확인합니다.

```bash
git --version
uv --version
code --version
```

**완료 기준:** Git·uv 버전이 출력되고 편집기가 열립니다. GUI가 없는 원격 서버에서는 편집기의 원격 연결 구성이 별도로 필요합니다. 이 가이드는 데스크톱 환경을 기준으로 합니다. [uv 설치](https://docs.astral.sh/uv/getting-started/installation/)

[03. Python 프로젝트 만들기로 이동](#project)
</details>

<details class="guide-os" id="windows" markdown="1">
<summary>Windows · 윈도에서 설치</summary>

### 2C-1. PowerShell 열기

이 가이드의 기본 경로는 **윈도에 직접 설치하는 방식**입니다. 시작 메뉴에서 **PowerShell**을 검색해 실행합니다. `PS C:\...>` 형태의 입력 줄을 확인합니다. WSL은 이 기본 실습의 필수 요소가 아닙니다.

### 2C-2. VS Code·Git·uv 설치

[VS Code 윈도 설치](https://code.visualstudio.com/docs/setup/windows)에 따라 설치 파일을 실행합니다. 다음은 PowerShell에서 실행합니다.

```powershell
winget install --id Git.Git -e --source winget
winget install --id astral-sh.uv -e
```

`winget`을 찾을 수 없다면 Git은 [공식 설치 파일](https://git-scm.com/install/windows)을 사용하고, uv는 [공식 안내의 Windows 설치 방법](https://docs.astral.sh/uv/getting-started/installation/)을 사용합니다. Cursor를 선택했다면 VS Code 대신 [Cursor 윈도 설치](https://cursor.com/docs/get-started/quickstart)를 진행합니다.

### 2C-3. 새 PowerShell에서 확인

열려 있던 터미널과 편집기를 닫았다가 다시 실행한 뒤 확인합니다.

```powershell
git --version
uv --version
code --version
```

**완료 기준:** Git·uv 버전이 출력되고 편집기가 열립니다. Cursor 사용자는 `code` 명령 대신 **File → Open Folder**를 이용합니다.

[03. Python 프로젝트 만들기로 이동](#project)
</details>

<details class="guide-os" id="windows-wsl" markdown="1">
<summary>선택 사항 · 윈도에서 리눅스 환경이 필요한 경우(WSL 2)</summary>

연구 코드가 Linux 도구를 요구할 때 선택합니다. 처음부터 Windows 기본 경로와 WSL을 번갈아 사용하지 말고, 한 실습은 한 환경에서 끝내세요.

1. **관리자 PowerShell**에서 아래 명령을 실행하고, 필요하면 컴퓨터를 다시 시작합니다.

```powershell
wsl --install
```

2. 설치된 Ubuntu를 열어 리눅스 사용자명과 암호를 정합니다. `wsl --list --verbose`로 버전이 `2`인지 확인합니다.
3. **윈도 쪽에 VS Code**, VS Code에 Microsoft의 **WSL 확장**을 설치합니다. Ubuntu 안에 데스크톱 VS Code를 다시 설치하지 않습니다.
4. **Ubuntu 터미널**에서 위 Linux 절차의 Git·curl·uv만 설치합니다. 프로젝트는 `~/projects` 아래에 만들고 `code .`로 엽니다. 편집기 왼쪽 아래에 WSL 연결 상태가 표시되는지 확인합니다.
5. 이후 Python·uv 명령은 WSL에 연결된 편집기의 터미널에서 실행합니다. AI 확장은 해당 확장의 WSL 안내와 **Install in WSL** 표시를 따릅니다. CLI 도구는 Ubuntu 쪽에 설치합니다.

윈도와 WSL의 Python·가상환경·경로는 서로 다릅니다. Windows에서 만든 `.venv`를 WSL에 복사하지 말고, 해당 환경에서 `uv sync`로 다시 만듭니다.

공식 안내: [WSL 설치](https://learn.microsoft.com/ko-kr/windows/wsl/install) · [WSL 개발 환경](https://learn.microsoft.com/ko-kr/windows/wsl/setup/environment) · [VS Code와 WSL](https://code.visualstudio.com/docs/remote/wsl)
</details>

{% include section.html %}

## 03. Python 프로젝트 만들기
{: #project }

### 3-1. 실습 폴더 만들기

**macOS·Linux·WSL 터미널:**

```bash
mkdir -p ~/projects
cd ~/projects
mkdir orbit-lab
cd orbit-lab
```

**Windows PowerShell:**

```powershell
New-Item -ItemType Directory -Force "$env:USERPROFILE\projects"
Set-Location "$env:USERPROFILE\projects"
New-Item -ItemType Directory orbit-lab
Set-Location orbit-lab
```

`orbit-lab`이 이미 있으면 새 이름을 사용합니다. 예를 들어 `orbit-lab-02`를 만들고 해당 폴더로 이동하세요. 아래는 **빈 실습 폴더 안에서** 실행합니다.

### 3-2. Python과 프로젝트 환경 준비

**모든 운영체제 공통:**

```bash
uv python install 3.12
uv init --bare --python 3.12
uv python pin 3.12
uv sync
uv run python --version
```

마지막에 `Python 3.12.x`가 표시되면 정상입니다. `3.12`는 이 문서의 실습 기준이며 최신 버전을 뜻하지 않습니다. `pyproject.toml`은 프로젝트 설정, `uv.lock`은 의존성 기록, `.python-version`은 Python 선택, `.venv`는 실행 환경입니다. `uv run`을 쓰므로 가상환경을 수동으로 활성화할 필요가 없습니다. [Python 설치](https://docs.astral.sh/uv/guides/install-python/) · [uv 프로젝트 만들기](https://docs.astral.sh/uv/concepts/projects/init/)

### 3-3. 편집기에서 폴더 열기

`code .`를 실행하거나 **File → Open Folder**에서 `orbit-lab`을 선택합니다. Microsoft의 **Python 확장**을 설치하고, 명령 팔레트에서 **Python: Select Interpreter**를 실행해 이 폴더의 `.venv`를 선택합니다.

- macOS·Linux·WSL: `.venv/bin/python`
- Windows: `.venv\Scripts\python.exe`

편집기 메뉴 **Terminal → New Terminal**에서 `uv run python --version`을 다시 실행합니다. 앞으로 명령은 이 터미널에 입력하세요. [VS Code Python 시작하기](https://code.visualstudio.com/docs/python/python-tutorial)

### 3-4. 첫 상태를 Git으로 저장

탐색기에서 **New File**을 눌러 `.gitignore` 파일을 만들고 다음 내용을 저장합니다.

```text
{% include guides/gitignore.txt %}
```

`README.md`도 만들고 `# Orbit Lab`이라는 제목을 저장합니다. 아래 이름·이메일은 **본인 정보로 바꾼 뒤** 실행합니다. 이 설정은 현재 실습 저장소에 적용됩니다.

```bash
git init -b main
git config user.name "Your Name"
git config user.email "your-email@example.com"
git add .gitignore .python-version pyproject.toml uv.lock README.md
git commit -m "Set up orbit exercise"
```

**완료 기준:** `git status`에 저장할 변경사항이 없다고 표시됩니다. Git 커밋은 내 컴퓨터의 기록이며, GitHub 업로드와는 별도입니다. [Git 사용자 설정](https://git-scm.com/book/ko/v2/시작하기-Git-최초-설정) · [.gitignore 안내](https://docs.github.com/en/get-started/git-basics/ignoring-files)

{% include section.html %}

## 04. AI 코딩 도구 하나 연결하기
{: #assistant }

아래 네 경로 중 하나를 선택합니다. **도구를 전부 설치하거나 모두 구독할 필요는 없습니다.** 인터페이스는 업데이트될 수 있으므로 버튼 이름이 다르면 연결된 공식 문서를 확인하세요.

<details class="guide-tool" markdown="1">
<summary>A. VS Code + Codex</summary>

1. [OpenAI 공식 Codex 확장 안내](https://learn.chatgpt.com/docs/codex/ide)의 설치 링크로 확장을 설치합니다.
2. `orbit-lab` 폴더에서 Codex 아이콘을 엽니다. 아이콘이 없으면 명령 팔레트에서 **Codex: Open Codex Sidebar**를 실행합니다.
3. 화면 안내에 따라 로그인합니다. 사용 가능한 인증 방식과 계정의 이용 조건을 확인합니다.
4. 채팅에 “현재 폴더의 파일과 Python 실행 방법을 설명해줘. 아직 파일은 수정하지 마.”라고 입력합니다.

**완료 기준:** AI가 현재 프로젝트의 `pyproject.toml`과 `uv run`을 설명합니다. Windows에서 실행 환경 설정을 요청하면 확장의 안내를 따릅니다.
</details>

<details class="guide-tool" markdown="1">
<summary>B. VS Code + Claude Code</summary>

1. [Anthropic 공식 VS Code 안내](https://code.claude.com/docs/ko/vs-code)에서 확장을 설치합니다.
2. Claude Code 패널을 열고 사용 가능한 Claude 계정으로 로그인합니다. 구독 또는 Console 사용 조건은 공식 안내에서 확인합니다.
3. `orbit-lab` 폴더를 열고 현재 프로젝트의 구조와 실행 방법을 설명해 달라고 요청합니다.

**완료 기준:** 프로젝트 파일을 참고한 답변이 나옵니다. 확장 채팅만 사용할 때는 별도의 터미널용 CLI 설치가 필요하지 않습니다. 터미널에서 `claude`를 실행하려면 아래의 선택 설치를 추가합니다.
</details>

<details class="guide-tool" markdown="1">
<summary>C. VS Code + GitHub Copilot</summary>

1. [공식 Copilot 설정 안내](https://code.visualstudio.com/docs/setup/copilot)를 열고 VS Code의 Copilot 메뉴에서 **Use AI Features** 또는 로그인 항목을 선택합니다.
2. GitHub 계정으로 로그인하고 제공되는 이용 범위를 확인합니다. 이용량과 추가 과금 조건은 계정에서 확인하세요.
3. 채팅의 **Agent** 기능을 선택해 `orbit-lab`의 구조를 설명해 달라고 요청합니다. 메뉴 위치는 [Agents 빠른 시작](https://code.visualstudio.com/docs/agents/quickstart)을 참고합니다.

**완료 기준:** 일반 질의응답을 넘어 열린 프로젝트를 읽고 필요한 파일 수정을 제안할 수 있습니다.
</details>

<details class="guide-tool" markdown="1">
<summary>D. Cursor</summary>

1. [Cursor 빠른 시작](https://cursor.com/docs/get-started/quickstart)에 따라 운영체제에 맞게 설치하고 로그인합니다.
2. **Open Folder**로 `orbit-lab`을 엽니다.
3. Agent 패널에서 파일 구조와 실행 방법을 설명해 달라고 요청합니다.
4. 파일을 수정한 뒤에는 변경 내역(diff)을 읽고 실행 결과를 확인합니다.

**완료 기준:** Cursor에서 실습 폴더와 AI 채팅, 터미널을 함께 사용할 수 있습니다.
</details>

<details class="guide-tool" markdown="1">
<summary>선택 사항 · 터미널에서 Codex 또는 Claude Code 사용</summary>

편집기 확장 대신 CLI를 쓰고 싶을 때만 설치합니다. 다음 명령은 각 회사의 공식 설치 스크립트를 실행합니다. 두 도구 중 사용할 도구만 고르세요.

**Codex — macOS·Linux·WSL:**

```bash
curl -fsSL https://chatgpt.com/codex/install.sh | sh
```

**Codex — Windows PowerShell:**

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://chatgpt.com/codex/install.ps1 | iex"
```

새 터미널의 `orbit-lab` 폴더에서 `codex`를 실행하고 로그인합니다. [OpenAI 공식 Codex CLI 안내](https://learn.chatgpt.com/docs/codex/cli)

**Claude Code — macOS·Linux·WSL:**

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

**Claude Code — Windows PowerShell:**

```powershell
irm https://claude.ai/install.ps1 | iex
```

새 터미널에서 `claude --version`을 확인한 뒤, `orbit-lab`에서 `claude`를 실행하고 로그인합니다. [Claude Code 빠른 시작](https://code.claude.com/docs/ko/quickstart)
</details>

{% include section.html %}

## 05. 첫 실습: 원궤도 속도와 주기 계산
{: #exercise }

지구 중심의 원궤도를 가정하고 고도에 따른 속도와 주기를 계산합니다. 아래 상수는 **실습을 위해 고정한 값**입니다. 구형 지구의 2체 문제로 단순화하며, 대기저항·지구 비구형 중력·제3체 섭동은 포함하지 않습니다.

| 입력·출력 | 정의 |
|---|---|
| `mu = 398600.4418` | 중력상수와 지구 질량의 곱, km³/s² |
| `R = 6378.137` | 이 실습에서 사용하는 기준 지구 반지름, km |
| `h` | 기준 표면으로부터의 고도, km |
| `r = R + h` | 지구 중심으로부터의 거리, km |
| `v = sqrt(mu / r)` | 원궤도 속도, km/s |
| `T = 2 * pi * sqrt(r^3 / mu)` | 공전주기, 초. 분으로 표시할 때 60으로 나눔 |

### 5-1. 먼저 계획을 요청하기

다음 문장을 **AI 채팅창**에 붙여넣습니다.

```text
이 폴더에서 Python 원궤도 계산 실습을 하려고 합니다.
먼저 파일 구성, 사용할 식, 입력·출력 단위와 검증 방법을 설명하세요.
아직 파일은 수정하지 마세요.

실습 조건:
- Python 3.12, 표준 라이브러리만 사용
- mu = 398600.4418 km^3/s^2, R = 6378.137 km
- 고도 h는 km이며 r = R + h
- 출력은 속도 km/s와 주기 min
- 구형 지구의 2체 원궤도, 섭동은 제외
```

설명에서 **고도와 지구 중심 거리**, **초와 분**을 구분했는지 확인합니다.

### 5-2. 구현과 실행 요청하기

```text
위 조건으로 orbit.py와 test_orbit.py를 작성하세요.
circular_orbit(altitude_km) 함수는 (속도 km/s, 주기 min)을 반환해야 합니다.
음수·NaN·무한대 고도는 ValueError로 처리하세요.
orbit.py를 직접 실행하면 400 km와 800 km 결과를 소수점 6자리로 출력하세요.
unittest로 기준 수치, 고도에 따른 변화, 잘못된 입력을 검증하세요.
uv run python orbit.py와 uv run python -m unittest -v로 실행하고,
변경한 파일과 실제 실행 결과를 설명하세요.
```

AI가 실행했다고 답했더라도, 터미널에서 아래 명령을 직접 실행합니다.

```bash
uv run python orbit.py
uv run python -m unittest -v
```

기준 출력은 다음과 같습니다. AI가 만든 출력 형식은 달라도 **수치와 단위**가 일치해야 합니다.

```text
h=400 km | v=7.668558 km/s | T=92.560405 min
h=800 km | v=7.451831 km/s | T=100.873559 min
```

### 5-3. 참고 코드와 비교

막히면 아래 코드를 같은 이름의 파일에 저장해 비교합니다. AI를 아직 연결하지 못했다면 이 코드로 먼저 Python 환경을 확인할 수 있습니다. [참고 코드 ZIP]({{ '/downloads/search-lab-ai-coding-starter.zip' | relative_url }})은 **별도 폴더에 압축을 풀어** 실행하는 완성 예제입니다. ZIP 안에서는 `uv init`을 다시 실행하지 않습니다.

<details class="guide-code" markdown="1">
<summary>orbit.py · 참고 구현 보기</summary>

```python
{% include guides/orbit.py %}
```
</details>

<details class="guide-code" markdown="1">
<summary>test_orbit.py · 검증 코드 보기</summary>

```python
{% include guides/test_orbit.py %}
```
</details>

{% include section.html %}

## 06. 검증하고 한 단계 확장하기
{: #verify }

**테스트 통과는 구현 확인의 일부입니다.** 다음 항목을 코드와 계산 결과에 대조하세요.

1. **단위:** 거리 km와 중력상수 km³/s²를 일관되게 썼는가? 주기는 초에서 분으로 변환했는가?
2. **기준값:** 400 km에서 약 7.668558 km/s, 92.560405분이 나오는가? 반올림 기준값과 비교할 때 허용 오차를 두었는가?
3. **경향:** 800 km에서는 속도가 줄고 주기가 늘어나는가?
4. **입력 검사:** 음수·NaN·무한대를 거부하는가? 0 km는 수학적 경계 사례일 뿐 실제 운용 가능한 궤도를 뜻하지 않음을 이해했는가?
5. **모델 범위:** 실제 위성의 정밀 궤도 예측과 이 원궤도 예제의 차이를 설명할 수 있는가?

참고 검증 코드를 사용하면 **4개 테스트가 통과하고 `OK`**가 표시됩니다. AI가 만든 테스트는 개수가 다를 수 있으므로 검사 내용도 읽습니다. 테스트에서 구현의 식을 그대로 반복하는 것만으로 만족하지 말고, 계산기나 별도 계산으로 얻은 기준값과 비교합니다. [Python unittest 안내](https://docs.python.org/3.12/library/unittest.html)

확장 실습에서는 다음과 같이 **한 가지 기능만** 추가합니다.

```text
기존 계산 함수와 테스트를 유지하세요.
200~2000 km 고도를 100 km 간격으로 계산하는 별도 스크립트를 만들고,
고도·속도·주기를 CSV로 저장하세요. 열 이름에 단위를 포함하세요.
기존 테스트를 다시 실행하고, CSV의 400 km 행을 기준값과 비교하세요.
```

그래프를 그리고 싶다면 `uv add matplotlib`으로 의존성을 기록한 뒤, AI에게 축 이름·단위·모델 가정을 표시하도록 요청합니다. `pyproject.toml`과 `uv.lock`도 함께 변경되는지 확인하세요. [uv 프로젝트와 의존성 관리](https://docs.astral.sh/uv/guides/projects/)

{% include section.html %}

## 07. 결과를 저장하고 다시 실행하기
{: #share }

### 7-1. README에 실습 기록 남기기

`README.md`에 목적, 가정과 상수, 실행 명령, 기준 결과, 테스트 결과, 사용한 AI 도구·주요 요청·직접 수정한 내용을 적습니다. `uv --version`과 `uv run python --version`의 출력도 기록하면 이후 환경 차이를 비교하기 쉽습니다.

### 7-2. 변경 내역 확인 후 커밋

```bash
git status
git diff
git add orbit.py test_orbit.py README.md pyproject.toml uv.lock .python-version .gitignore
git diff --cached
git commit -m "Add and verify circular orbit calculation"
```

`git diff`는 아직 Git이 추적하지 않는 새 파일의 내용을 보여주지 않습니다. `git status`로 파일 목록을 확인하고, `git add` 후 `git diff --cached`에서 새 파일까지 읽습니다. 확장 실습 파일은 내용을 확인해 파일명으로 추가합니다.

### 7-3. GitHub 공유는 필요할 때

VS Code의 **Source Control → Publish to GitHub**로 로그인하고 저장소 이름과 공개 범위를 선택할 수 있습니다. 팀에서 함께 사용할 자료라면 공유할 파일을 검토한 뒤 게시합니다. 기존 저장소에 연결하는 방법과 인증은 [GitHub 원격 저장소에 push하기](https://docs.github.com/en/get-started/using-git/pushing-commits-to-a-remote-repository)를 참고합니다.

### 7-4. 다른 컴퓨터에서 재현

저장소를 복제하거나 프로젝트 파일을 전달받은 뒤, **`uv.lock`이 들어 있는 프로젝트 폴더**에서 실행합니다.

```bash
uv sync --locked
uv run python orbit.py
uv run python -m unittest -v
```

`.venv`는 복사하지 않고 컴퓨터마다 다시 만듭니다. `.python-version`의 `3.12`는 같은 계열을 선택하며 패치 버전까지 같게 고정하지는 않습니다. 엄밀한 연구 재현에는 실제 Python 패치 버전, 운영체제, 입력 데이터, 난수 시드와 수치해석 설정도 기록합니다. [uv 환경 동기화](https://docs.astral.sh/uv/concepts/projects/sync/)

**실습 완료 기준:** 궤도 계산과 테스트를 다시 실행할 수 있고, 계산 가정과 결과를 설명하며, Git에 검증된 상태가 남아 있습니다.

{% include section.html %}

## 08. 자주 만나는 문제
{: #troubleshooting }

| 증상 | 먼저 확인할 내용 |
|---|---|
| `uv` 또는 `git`을 찾을 수 없음 | 설치가 완료됐는지 확인하고 터미널·편집기를 완전히 재시작합니다. 계속 안 되면 해당 공식 설치 문서의 PATH 안내를 확인합니다. |
| `code` 명령이 없음 | 맥은 명령 팔레트에서 PATH 등록을 실행합니다. 우선 File → Open Folder로 폴더를 열어도 됩니다. |
| Windows에서 명령 문법 오류 | 현재 창이 PowerShell인지 확인합니다. bash 명령과 PowerShell 명령을 섞지 않습니다. |
| 이미 `pyproject.toml`이 있다고 표시됨 | 기존 프로젝트 또는 ZIP 예제입니다. `uv init`을 생략하고 `uv sync`를 실행합니다. |
| Python 버전이 다름 | 실습 폴더에서 `uv run python --version`을 확인합니다. `python --version`은 시스템 Python을 가리킬 수 있습니다. |
| `orbit.py`를 찾을 수 없음 | 파일을 저장했는지, 터미널의 현재 위치가 `orbit-lab`인지 확인합니다. 윈도의 숨겨진 확장자 때문에 `.py.txt`가 되지 않았는지도 봅니다. |
| `ModuleNotFoundError` | `uv run`으로 실행하고 있는지 확인합니다. 추가 라이브러리는 `uv add 패키지명`으로 현재 프로젝트에 설치합니다. |
| AI가 다른 프로젝트를 설명함 | 편집기와 AI가 참조하는 작업 폴더를 `orbit-lab`으로 맞춥니다. |
| AI 로그인·사용량 오류 | 계정·선택 모델·이용 한도를 확인합니다. 기본 실습은 참고 코드로 계속할 수 있습니다. |
| 테스트가 `Ran 0 tests`라고 나옴 | 파일명을 `test_orbit.py`, 메서드명을 `test_`로 시작하도록 확인합니다. 0개 통과는 검증 완료가 아닙니다. |
| Git에서 작성자 정보 오류 | 현재 저장소의 `git config user.name`과 `git config user.email`을 설정합니다. |
| WSL에서만 도구를 찾지 못함 | 윈도에 설치한 도구와 WSL 안의 도구를 구분합니다. Ubuntu 터미널에서 Git·uv·Python을 다시 확인합니다. |

오류를 AI에게 물을 때에는 **운영체제, 실행한 명령, 오류 전문, 기대한 결과**를 함께 전달하세요. 예를 들어 “Windows PowerShell에서 `uv run python orbit.py`를 실행했는데 다음 오류가 발생했다”처럼 적으면 원인을 좁힐 수 있습니다.

{% include section.html %}

## 09. 공식 문서 모음
{: #references }

이 가이드는 아래 문서의 설치·프로젝트·실행·검증 관련 내용을 참고해 학생 실습 순서로 재구성했습니다. 공식 문서를 그대로 번역한 문서는 아니며, 궤도 계산과 검증 코드는 SEARCH Lab용으로 작성한 교육 예제입니다. 설치 화면과 명령은 바뀔 수 있으므로 문제가 생기면 해당 공식 안내를 확인하세요.

| 구분 | 공식 자료 |
|---|---|
| VS Code 설치 | [macOS](https://code.visualstudio.com/docs/setup/mac) · [Linux](https://code.visualstudio.com/docs/setup/linux) · [Windows](https://code.visualstudio.com/docs/setup/windows) |
| Python 편집 환경 | [Python in VS Code](https://code.visualstudio.com/docs/python/python-tutorial) |
| Git | [운영체제별 설치](https://git-scm.com/install/) · [최초 설정](https://git-scm.com/book/ko/v2/시작하기-Git-최초-설정) |
| uv | [설치](https://docs.astral.sh/uv/getting-started/installation/) · [Python 관리](https://docs.astral.sh/uv/guides/install-python/) · [프로젝트](https://docs.astral.sh/uv/guides/projects/) · [잠금·동기화](https://docs.astral.sh/uv/concepts/projects/sync/) |
| macOS 패키지 관리 | [Homebrew 한국어 안내](https://brew.sh/ko/) |
| WSL | [설치](https://learn.microsoft.com/ko-kr/windows/wsl/install) · [개발 환경](https://learn.microsoft.com/ko-kr/windows/wsl/setup/environment) · [VS Code 연결](https://code.visualstudio.com/docs/remote/wsl) |
| OpenAI Codex | [편집기 확장](https://learn.chatgpt.com/docs/codex/ide) · [CLI](https://learn.chatgpt.com/docs/codex/cli) |
| Claude Code | [한국어 빠른 시작](https://code.claude.com/docs/ko/quickstart) · [상세 설정](https://code.claude.com/docs/ko/setup) · [VS Code 확장](https://code.claude.com/docs/ko/vs-code) |
| GitHub Copilot | [설정](https://code.visualstudio.com/docs/setup/copilot) · [Agent 실습](https://code.visualstudio.com/docs/agents/quickstart) |
| Cursor | [설치와 첫 작업](https://cursor.com/docs/get-started/quickstart) |
| 테스트 | [Python unittest](https://docs.python.org/3.12/library/unittest.html) |
| GitHub 공유 | [저장소 만들기](https://docs.github.com/ko/get-started/start-your-journey/creating-a-repository-for-your-project-on-github) · [원격 저장소에 push](https://docs.github.com/en/get-started/using-git/pushing-commits-to-a-remote-repository) |

<div class="resource-related">
  <a class="text-link" href="{{ '/students/' | relative_url }}">학생 연구자 안내로 돌아가기 <span aria-hidden="true">→</span></a>
  <a class="text-link" href="{{ '/links/' | relative_url }}">진학·연구 자료 더 보기 <span aria-hidden="true">→</span></a>
</div>
