---
title: AI Coding Guide
ref: ai-coding-guide
parent_ref: students
description: Set up AI-assisted coding on macOS, Linux or Windows, then build, verify and version a Python orbit calculation.
---

<p class="guide-breadcrumb"><a href="{{ '/en/students/' | relative_url }}">For Students</a> <span aria-hidden="true">/</span> Practical guide</p>

# AI Coding Guide for Student Researchers
{: .page-title }

Set up your computer, build a small orbit calculation with an AI assistant, and learn to run, verify and save your work.
{: .page-intro }

<div class="guide-meta"><span>Beginner · Python</span><span>60–90 minutes + installation</span><span>Docs checked: October 5, 2026</span></div>
<div class="guide-actions">
  <a class="guide-button" href="#setup">Choose your operating system <span aria-hidden="true">↓</span></a>
  <a class="guide-button guide-button-secondary" href="{{ '/downloads/search-lab-ai-coding-starter.zip' | relative_url }}" download>Reference code ZIP</a>
  <button class="guide-button guide-button-secondary" type="button" data-guide-print hidden>Print · Save as PDF</button>
</div>

<nav class="guide-toc" aria-label="Guide contents" markdown="1">
1. [Tools and workflow](#start)
2. [Install for your OS](#setup)
3. [Create a Python project](#project)
4. [Connect one AI assistant](#assistant)
5. [Calculate a circular orbit](#exercise)
6. [Verify and extend](#verify)
7. [Save and reproduce](#share)
8. [Troubleshooting](#troubleshooting)
9. [Official documentation](#references)
</nav>

{% include section.html %}

## 01. Tools and workflow
{: #start }

Here, **vibe coding** means describing a task in natural language and building code with AI assistance. For research, the workflow also includes understanding the assumptions and units and checking the results independently.

| Component | Purpose | Used here |
|---|---|---|
| Editor | Open and edit project files | VS Code or Cursor |
| Git | Record changes and recovery points | All operating systems |
| Python + uv | Run calculations and manage project environments | Python 3.12 series |
| AI assistant | Explain, write and improve code | Choose Codex, Claude Code, Copilot or Cursor |

Start with **VS Code + Git + uv**, then choose one assistant that your account supports. If you choose Cursor, use it as your editor instead. The file and terminal exercises work in either editor. You need a GitHub account only for the optional online sharing step. AI access, allowances and costs depend on your service and account; check them when signing in. Node.js, Docker and a GPU are not needed for the basic exercise.

Enter commands in a **terminal** and requests to the assistant in its **chat panel**. Run commands one line at a time, resolving any error before continuing. This exercise uses public numerical values and a purpose-written example.

{% include section.html %}

## 02. Install for your operating system
{: #setup }

Choose **one** route. If a tool is already installed, check its version and skip that installation.

<div class="guide-os-links">
  <a href="#macos">macOS <span>Terminal</span></a>
  <a href="#linux">Linux <span>Ubuntu · Debian · Fedora</span></a>
  <a href="#windows">Windows <span>PowerShell</span></a>
</div>

<details class="guide-os" id="macos" markdown="1">
<summary>macOS · Install on a Mac</summary>

### 2A-1. Install your editor

1. [Download VS Code](https://code.visualstudio.com/download) for your processor: Apple Silicon or Intel.
2. Move the application to **Applications** and open it.
3. Press `Cmd+Shift+P` and run **Shell Command: Install 'code' command in PATH**. Open a new terminal afterwards.

For Cursor, use its [quickstart](https://cursor.com/docs/get-started/quickstart). Open your project with **File → Open Folder** instead of `code .`.

### 2A-2. Install Git

Find **Terminal** in Spotlight, open it, and run:

```bash
git --version
```

If a version appears, continue. If prompted to install developer tools, complete that installation. If Git is unavailable and no prompt appears, run:

```bash
xcode-select --install
```

If you already use Homebrew, `brew install git` is an alternative. Choose one installation method. [Git on macOS](https://git-scm.com/install/mac) · [Homebrew](https://brew.sh/)

### 2A-3. Install uv and check

This command downloads and runs uv's official installer:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Close and reopen Terminal, then run:

```bash
git --version
uv --version
code --version
```

**Checkpoint:** Git and uv report versions, and your editor opens. If `code` is unavailable, use **File → Open Folder**. [VS Code macOS setup](https://code.visualstudio.com/docs/setup/mac) · [uv installation](https://docs.astral.sh/uv/getting-started/installation/)

[Continue to 03. Create a Python project](#project)
</details>

<details class="guide-os" id="linux" markdown="1">
<summary>Linux · Install on your distribution</summary>

### 2B-1. Install Git and curl

On Ubuntu or Debian:

```bash
sudo apt update
sudo apt install git curl
```

On Fedora:

```bash
sudo dnf install git curl
```

See [Git for Linux](https://git-scm.com/install/linux) for other distributions. Your password may not be visible while typing at a `sudo` prompt; press Enter when finished.

### 2B-2. Install your editor

Follow [VS Code's Linux guide](https://code.visualstudio.com/docs/setup/linux). Download the package matching your distribution and processor: `.deb` for Ubuntu/Debian, `.rpm` for Fedora. Open it in your software installer. For Cursor, use its [Linux instructions](https://cursor.com/docs/get-started/quickstart).

### 2B-3. Install uv and check

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

In a new terminal:

```bash
git --version
uv --version
code --version
```

**Checkpoint:** Git and uv report versions, and your editor opens. This guide assumes a desktop environment; a headless server needs a separate remote-editor setup. [uv installation](https://docs.astral.sh/uv/getting-started/installation/)

[Continue to 03. Create a Python project](#project)
</details>

<details class="guide-os" id="windows" markdown="1">
<summary>Windows · Install with PowerShell</summary>

### 2C-1. Open PowerShell

The default route runs directly on Windows. Search for **PowerShell** in Start; its prompt normally starts with `PS C:\...>`. WSL is optional for this exercise.

### 2C-2. Install VS Code, Git and uv

Run the installer in [VS Code's Windows guide](https://code.visualstudio.com/docs/setup/windows). Then run these commands in PowerShell:

```powershell
winget install --id Git.Git -e --source winget
winget install --id astral-sh.uv -e
```

If `winget` is unavailable, use the [Git installer](https://git-scm.com/install/windows) and the Windows method in [uv's installation guide](https://docs.astral.sh/uv/getting-started/installation/). For Cursor, follow its [Windows setup](https://cursor.com/docs/get-started/quickstart) instead of installing VS Code.

### 2C-3. Reopen and check

Close your terminals and editor and reopen them before checking:

```powershell
git --version
uv --version
code --version
```

**Checkpoint:** Git and uv report versions, and your editor opens. Cursor users can use **File → Open Folder** instead of `code`.

[Continue to 03. Create a Python project](#project)
</details>

<details class="guide-os" id="windows-wsl" markdown="1">
<summary>Optional · Linux tools on Windows with WSL 2</summary>

Choose this route when your research code requires Linux tools. Finish one exercise in one environment rather than switching between native Windows and WSL.

1. In **administrator PowerShell**, run the following and restart if requested:

```powershell
wsl --install
```

2. Open Ubuntu and set your Linux username and password. Check that `wsl --list --verbose` reports version `2`.
3. Install **VS Code on Windows** and its Microsoft **WSL extension**. Do not install the desktop editor again inside Ubuntu.
4. In the **Ubuntu terminal**, follow the Linux steps above for Git, curl and uv only. Keep projects under `~/projects`, then open them with `code .`. Check the editor's WSL connection indicator.
5. Run Python and uv inside the connected editor's WSL terminal. Follow each AI extension's WSL instructions or **Install in WSL** prompt; install CLI assistants inside Ubuntu.

Windows and WSL have separate Python environments and paths. Recreate `.venv` with `uv sync` instead of copying it between systems.

[Install WSL](https://learn.microsoft.com/en-us/windows/wsl/install) · [Development environment](https://learn.microsoft.com/en-us/windows/wsl/setup/environment) · [VS Code in WSL](https://code.visualstudio.com/docs/remote/wsl)
</details>

{% include section.html %}

## 03. Create a Python project
{: #project }

### 3-1. Create an exercise folder

**macOS, Linux or WSL terminal:**

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

If `orbit-lab` exists, choose a new name, such as `orbit-lab-02`, and enter that folder. Run the next commands **inside the empty exercise folder**.

### 3-2. Prepare Python and the environment

**All operating systems:**

```bash
uv python install 3.12
uv init --bare --python 3.12
uv python pin 3.12
uv sync
uv run python --version
```

Expect `Python 3.12.x`. This is the exercise baseline, not a claim about the latest release. `pyproject.toml` holds settings, `uv.lock` records dependencies, `.python-version` selects Python, and `.venv` contains the environment. `uv run` avoids manual activation. [Install Python](https://docs.astral.sh/uv/guides/install-python/) · [Create a uv project](https://docs.astral.sh/uv/concepts/projects/init/)

### 3-3. Open the folder in your editor

Run `code .` or use **File → Open Folder**. Install Microsoft's **Python extension**. In the Command Palette, run **Python: Select Interpreter** and choose your project's `.venv`:

- macOS/Linux/WSL: `.venv/bin/python`
- Windows: `.venv\Scripts\python.exe`

Open **Terminal → New Terminal** and check `uv run python --version` again. Use this terminal for subsequent commands. [Python in VS Code](https://code.visualstudio.com/docs/python/python-tutorial)

### 3-4. Save the starting point with Git

Use **New File** in the editor to create `.gitignore` with this content:

```text
{% include guides/gitignore.txt %}
```

Create `README.md` containing `# Orbit Lab`. Replace the name and email below with your own before running the commands. These settings apply to this repository.

```bash
git init -b main
git config user.name "Your Name"
git config user.email "your-email@example.com"
git add .gitignore .python-version pyproject.toml uv.lock README.md
git commit -m "Set up orbit exercise"
```

**Checkpoint:** `git status` reports a clean working tree. A commit records work locally; it does not upload to GitHub. [Git setup](https://git-scm.com/book/en/v2/Getting-Started-First-Time-Git-Setup) · [Ignoring files](https://docs.github.com/en/get-started/git-basics/ignoring-files)

{% include section.html %}

## 04. Connect one AI assistant
{: #assistant }

Choose one route. You do not need to install or subscribe to every service. If the interface differs, follow the current official guide.

<details class="guide-tool" markdown="1">
<summary>A. VS Code + Codex</summary>

1. Install the extension linked in the [official OpenAI Codex guide](https://learn.chatgpt.com/docs/codex/ide).
2. Open `orbit-lab` and select the Codex icon, or run **Codex: Open Codex Sidebar** from the Command Palette.
3. Follow sign-in and account-access prompts. On Windows, follow any environment-setup prompts.
4. Ask: “Explain this folder and how to run its Python code. Do not edit files yet.”

**Checkpoint:** The response refers to this project's `pyproject.toml` and `uv run`.
</details>

<details class="guide-tool" markdown="1">
<summary>B. VS Code + Claude Code</summary>

1. Install the extension from [Anthropic's VS Code guide](https://code.claude.com/docs/en/vs-code).
2. Open its panel and sign in with a supported Claude account. Check subscription or Console requirements in the official guide.
3. Open `orbit-lab` and ask it to explain the project and execution commands.

**Checkpoint:** The response uses the current files. Extension chat does not require a separate CLI installation; running `claude` in a terminal does.
</details>

<details class="guide-tool" markdown="1">
<summary>C. VS Code + GitHub Copilot</summary>

1. Follow the [Copilot setup guide](https://code.visualstudio.com/docs/setup/copilot), selecting **Use AI Features** or sign-in from the Copilot menu.
2. Sign in with GitHub and check your account's allowance and billing conditions.
3. Use **Agent** to ask about the open project. See the [Agents quickstart](https://code.visualstudio.com/docs/agents/quickstart) for the current interface.

**Checkpoint:** The assistant can use project files and propose edits.
</details>

<details class="guide-tool" markdown="1">
<summary>D. Cursor</summary>

1. Install and sign in using [Cursor's quickstart](https://cursor.com/docs/get-started/quickstart).
2. Open `orbit-lab` with **Open Folder**.
3. Ask Agent to explain the files and execution commands.
4. Inspect the diff and run the code after each change.

**Checkpoint:** Your project, agent chat and terminal are available in Cursor.
</details>

<details class="guide-tool" markdown="1">
<summary>Optional · Use Codex or Claude Code in a terminal</summary>

Use this route if you prefer a CLI. Choose one tool. These commands run the providers' official installers.

**Codex — macOS/Linux/WSL:**

```bash
curl -fsSL https://chatgpt.com/codex/install.sh | sh
```

**Codex — Windows PowerShell:**

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://chatgpt.com/codex/install.ps1 | iex"
```

Reopen your terminal, enter `orbit-lab`, run `codex`, and sign in. [Codex CLI](https://learn.chatgpt.com/docs/codex/cli)

**Claude Code — macOS/Linux/WSL:**

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

**Claude Code — Windows PowerShell:**

```powershell
irm https://claude.ai/install.ps1 | iex
```

In a new terminal, check `claude --version`, enter `orbit-lab`, run `claude`, and sign in. [Claude Code quickstart](https://code.claude.com/docs/en/quickstart)
</details>

{% include section.html %}

## 05. Calculate a circular orbit
{: #exercise }

Use a circular two-body model about Earth. The following are **fixed exercise constants**. The model assumes a spherical Earth and excludes drag, nonspherical gravity and third-body perturbations.

| Quantity | Definition |
|---|---|
| `mu = 398600.4418` | Gravitational parameter, km³/s² |
| `R = 6378.137` | Reference Earth radius used in this exercise, km |
| `h` | Altitude above the reference surface, km |
| `r = R + h` | Distance from Earth's center, km |
| `v = sqrt(mu / r)` | Circular speed, km/s |
| `T = 2 * pi * sqrt(r^3 / mu)` | Period in seconds; divide by 60 for minutes |

### 5-1. Ask for a plan

Paste this into the **AI chat panel**:

```text
Plan a Python circular-orbit exercise in this folder.
Explain the files, equations, input/output units and validation approach first.
Do not edit files yet.
Use Python 3.12 and only its standard library.
Use mu = 398600.4418 km^3/s^2 and R = 6378.137 km.
Altitude h is in km; r = R + h.
Return speed in km/s and period in minutes.
Assume a spherical-Earth two-body circular orbit without perturbations.
```

Check that the explanation distinguishes **altitude from center distance** and **seconds from minutes**.

### 5-2. Request implementation and execution

```text
Implement orbit.py and test_orbit.py using those assumptions.
circular_orbit(altitude_km) must return (speed_km_s, period_min).
Reject negative, NaN and infinite altitudes with ValueError.
When run directly, orbit.py must print results for 400 and 800 km
to six decimal places.
Use unittest to check reference values, trends with altitude and invalid input.
Run uv run python orbit.py and uv run python -m unittest -v.
Explain the changes and report actual execution results.
```

Run the commands yourself as well:

```bash
uv run python orbit.py
uv run python -m unittest -v
```

Expected numerical output; the generated formatting may differ:

```text
h=400 km | v=7.668558 km/s | T=92.560405 min
h=800 km | v=7.451831 km/s | T=100.873559 min
```

### 5-3. Compare the reference implementation

Save the following snippets under the indicated filenames if you get stuck. You can also use them to check Python before connecting an AI account. The [reference ZIP]({{ '/downloads/search-lab-ai-coding-starter.zip' | relative_url }}) is a completed example: extract it into a **separate folder** and follow its README. Do not run `uv init` inside the completed example.

<details class="guide-code" markdown="1">
<summary>orbit.py · Reference calculation</summary>

```python
{% include guides/orbit.py %}
```
</details>

<details class="guide-code" markdown="1">
<summary>test_orbit.py · Reference checks</summary>

```python
{% include guides/test_orbit.py %}
```
</details>

{% include section.html %}

## 06. Verify and extend
{: #verify }

Passing tests is one part of verification. Check the code and results against these questions:

1. **Units:** Are km and km³/s² consistent? Is the period converted to minutes?
2. **Reference:** At 400 km, do you obtain approximately 7.668558 km/s and 92.560405 minutes, with a tolerance for rounding?
3. **Trend:** At 800 km, is the speed lower and period longer?
4. **Inputs:** Are negative, NaN and infinite altitudes rejected? Zero altitude is a mathematical boundary case, not an operational orbit.
5. **Scope:** Can you explain why this example is different from precise satellite orbit prediction?

The reference implementation runs **four tests and reports `OK`**. AI-generated tests may have a different count: read what they check. Compare with an independent calculator or calculation rather than only repeating the implementation's formula in a test. [Python unittest](https://docs.python.org/3.12/library/unittest.html)

Add one feature at a time:

```text
Keep the existing calculation function and tests.
Add a separate script that computes altitudes from 200 to 2000 km
in 100 km steps, saving altitude, speed and period to CSV.
Include units in column names. Rerun the existing tests and compare
the CSV's 400 km row against the reference result.
```

For plots, run `uv add matplotlib`, then request labeled axes, units and model assumptions. Check that `pyproject.toml` and `uv.lock` record the new dependency. [uv projects](https://docs.astral.sh/uv/guides/projects/)

{% include section.html %}

## 07. Save and reproduce
{: #share }

### 7-1. Record the exercise

In `README.md`, record the objective, assumptions, constants, commands, reference results, test results, AI tool and key prompts, and changes you made yourself. Also record `uv --version` and `uv run python --version`.

### 7-2. Review and commit

```bash
git status
git diff
git add orbit.py test_orbit.py README.md pyproject.toml uv.lock .python-version .gitignore
git diff --cached
git commit -m "Add and verify circular orbit calculation"
```

`git diff` does not show untracked new files. Check the list with `git status`, then read new files too in `git diff --cached` after staging. Add any extension-exercise files explicitly after reviewing them.

### 7-3. Share on GitHub when needed

In VS Code, use **Source Control → Publish to GitHub**, sign in and choose a repository name and visibility. Review the files before sharing them with collaborators. For an existing remote repository and authentication, see [GitHub's push guide](https://docs.github.com/en/get-started/using-git/pushing-commits-to-a-remote-repository).

### 7-4. Reproduce on another computer

Clone or obtain the project, then run the following **in the folder containing its committed `uv.lock`**:

```bash
uv sync --locked
uv run python orbit.py
uv run python -m unittest -v
```

Recreate `.venv` on each computer rather than copying it. A `.python-version` of `3.12` selects that series, not an exact patch release. Rigorous research reproducibility also requires recording the Python patch version, OS, input data, random seeds and numerical settings. [uv locking and syncing](https://docs.astral.sh/uv/concepts/projects/sync/)

**Finished:** You can rerun the calculation and tests, explain the model and results, and recover the verified state from Git.

{% include section.html %}

## 08. Troubleshooting
{: #troubleshooting }

| Symptom | First check |
|---|---|
| `uv` or `git` not found | Confirm installation, then restart the terminal and editor. Follow the official installer's PATH instructions if necessary. |
| `code` not found | On macOS, install its PATH command from the Command Palette. File → Open Folder also works. |
| Windows syntax error | Confirm you are in PowerShell. Do not mix Bash and PowerShell command blocks. |
| `pyproject.toml` already exists | You are in an existing project or the completed ZIP. Skip `uv init` and run `uv sync`. |
| Unexpected Python version | Use `uv run python --version` inside the project; plain `python` may refer to a system installation. |
| Cannot find `orbit.py` | Save the file and check your current folder. On Windows, make sure it is not named `orbit.py.txt`. |
| `ModuleNotFoundError` | Run through `uv run`. Add extra packages with `uv add package-name` inside this project. |
| AI describes another project | Check both the editor's open folder and the assistant's working directory. |
| AI sign-in or usage error | Check the account, model access and allowance. Continue the Python exercise with the reference code if needed. |
| `Ran 0 tests` | Check `test_orbit.py` and method names beginning with `test_`. Zero tests is not successful validation. |
| Git identity error | Set this repository's `git config user.name` and `git config user.email`. |
| Tool missing only in WSL | Check Git, uv and Python inside Ubuntu; Windows installations are separate. |

When requesting help, include your **OS, exact command, complete error and expected result**. This makes a useful debugging prompt.

{% include section.html %}

## 09. Official documentation
{: #references }

This guide reorganizes the installation, project, execution and validation instructions below into a student exercise. It is not a verbatim translation. The orbit example was written for SEARCH Lab. Interfaces and commands may change; consult the relevant official guide when troubleshooting.

| Topic | Official references |
|---|---|
| VS Code | [macOS](https://code.visualstudio.com/docs/setup/mac) · [Linux](https://code.visualstudio.com/docs/setup/linux) · [Windows](https://code.visualstudio.com/docs/setup/windows) |
| Python editor | [Python in VS Code](https://code.visualstudio.com/docs/python/python-tutorial) |
| Git | [Install](https://git-scm.com/install/) · [Initial setup](https://git-scm.com/book/en/v2/Getting-Started-First-Time-Git-Setup) |
| uv | [Install](https://docs.astral.sh/uv/getting-started/installation/) · [Python](https://docs.astral.sh/uv/guides/install-python/) · [Projects](https://docs.astral.sh/uv/guides/projects/) · [Locking and syncing](https://docs.astral.sh/uv/concepts/projects/sync/) |
| macOS packages | [Homebrew](https://brew.sh/) |
| WSL | [Install](https://learn.microsoft.com/en-us/windows/wsl/install) · [Environment](https://learn.microsoft.com/en-us/windows/wsl/setup/environment) · [VS Code](https://code.visualstudio.com/docs/remote/wsl) |
| OpenAI Codex | [IDE extension](https://learn.chatgpt.com/docs/codex/ide) · [CLI](https://learn.chatgpt.com/docs/codex/cli) |
| Claude Code | [Quickstart](https://code.claude.com/docs/en/quickstart) · [Setup](https://code.claude.com/docs/en/setup) · [VS Code](https://code.claude.com/docs/en/vs-code) |
| GitHub Copilot | [Setup](https://code.visualstudio.com/docs/setup/copilot) · [Agent quickstart](https://code.visualstudio.com/docs/agents/quickstart) |
| Cursor | [Install and first task](https://cursor.com/docs/get-started/quickstart) |
| Tests | [Python unittest](https://docs.python.org/3.12/library/unittest.html) |
| GitHub | [Create a repository](https://docs.github.com/en/get-started/start-your-journey/creating-a-repository-for-your-project-on-github) · [Push commits](https://docs.github.com/en/get-started/using-git/pushing-commits-to-a-remote-repository) |

<div class="resource-related">
  <a class="text-link" href="{{ '/en/students/' | relative_url }}">Back to For Students <span aria-hidden="true">→</span></a>
  <a class="text-link" href="{{ '/en/links/' | relative_url }}">More study and research resources <span aria-hidden="true">→</span></a>
</div>
