# Student AI coding guide

The Korean and English guides are in `students/ai-coding/index.md` and
`en/students/ai-coding/index.md`. Both use the same runnable examples in
`_includes/guides/`; the snippets are included in fenced code blocks by Liquid.

After editing the examples, run `python3 _guides/package.py` to rebuild
`downloads/search-lab-ai-coding-starter.zip`. The archive is deterministic,
contains no virtual environment, credentials, Git metadata or external packages,
and includes instructions in its README.

Validate the extracted archive with `uv sync`, `uv run python orbit.py` and
`uv run python -m unittest -v`. Build Jekyll and check both languages, OS section
links, narrow screens, dark mode, and print layout. The guide's Print/PDF button
expands all details before printing and restores them afterwards.

Review external installation commands against the linked official documentation
when updating the guide. Update the reviewed date in both language pages and in
the package metadata only after that review; it is not an automated freshness date.
