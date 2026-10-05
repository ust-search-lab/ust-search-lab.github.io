"""Build the downloadable, dependency-free guide example from shared sources."""
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

ROOT = Path(__file__).resolve().parents[1]
DESTINATION = ROOT / "downloads/search-lab-ai-coding-starter.zip"
FILES = {
    "orbit.py": (ROOT / "_includes/guides/orbit.py").read_text(),
    "test_orbit.py": (ROOT / "_includes/guides/test_orbit.py").read_text(),
    ".gitignore": (ROOT / "_includes/guides/gitignore.txt").read_text(),
    ".python-version": "3.12\n",
    "pyproject.toml": '''[project]
name = "orbit-lab"
version = "0.1.0"
description = "SEARCH Lab AI-assisted coding tutorial"
requires-python = ">=3.12"
dependencies = []
''',
    "README.md": '''# SEARCH Lab · AI coding exercise

한국어 가이드: https://ust-search-lab.github.io/students/ai-coding/
English guide: https://ust-search-lab.github.io/en/students/ai-coding/

## 실행 / Run

Install Git, uv and an editor using the guide. Extract this archive to a NEW
folder, open the folder containing pyproject.toml in your editor, then run:

```sh
uv sync
uv run python orbit.py
uv run python -m unittest -v
```

Python 3.12 is selected by .python-version; uv can download it if absent.
No third-party Python packages are needed. uv sync generates uv.lock locally.
Do NOT run uv init inside this completed example.

이 ZIP은 완성된 참고 코드입니다. 별도 폴더에 압축을 풀고 실행하세요.
처음부터 따라 할 때는 가이드의 빈 프로젝트 만들기 절차를 사용하세요.

## Expected output

```text
h=400 km | v=7.668558 km/s | T=92.560405 min
h=800 km | v=7.451831 km/s | T=100.873559 min
```

The four unittest cases should pass (OK).

## Model

Circular two-body orbit, using the exercise constants mu = 398600.4418 km^3/s^2
and reference Earth radius = 6378.137 km. Radius is Earth radius PLUS altitude.
Speed = sqrt(mu/r); period = 2*pi*sqrt(r^3/mu), converted from seconds to minutes.
These are tutorial assumptions, not a precision orbit prediction. Drag,
oblateness, third-body gravity and real mission conditions are omitted.
Zero altitude is a mathematical boundary case, not a usable physical orbit.

## Reproduce / 재현

Record the output of uv --version and uv run python --version in your research
notes. Keep pyproject.toml, uv.lock, .python-version, source and tests in Git.
For a copied or cloned project with a committed uv.lock, run uv sync --locked.

Guide reviewed: 2026-10-05. This example was authored for SEARCH Lab.
''',
}

DESTINATION.parent.mkdir(exist_ok=True)
with ZipFile(DESTINATION, "w", compression=ZIP_DEFLATED) as archive:
    for name, content in FILES.items():
        info = ZipInfo(f"orbit-lab/{name}", (2026, 10, 5, 0, 0, 0))
        info.compress_type = ZIP_DEFLATED
        info.external_attr = 0o100644 << 16
        archive.writestr(info, content.encode("utf-8"))
print(DESTINATION)
