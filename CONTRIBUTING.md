# Contributing

Use Python 3.11+ plus `actionlint`.

Run the local checks with:

```sh
actionlint && python3 -m unittest discover -s tests -v
```

The fixtures exercise semantic-version and date-only legacy release histories. They do not make network calls.

For an integration check, create a disposable repository with `CHANGELOG.md` and a literal `[project] version` in `pyproject.toml`, add the release wrapper from `examples/`, and dispatch `0.2.0` on its default branch. Expect one `chore(release): 0.2.0` commit, tag `v0.2.0` on that commit, an empty `Unreleased` section, and release notes copied from the former section. Do not run this against a consumer repository until its branch protection permits the workflow token to write.

Release this repository by merging a reviewed change, tagging it, then updating consumer workflow SHA pins deliberately. Its own validation workflow does not call itself.
