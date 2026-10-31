# github-workflows

Small reusable GitHub Actions workflows for Diletta's Python repositories.

## Pull request policy

Use `examples/pull-request-policy.yml` as the caller. Pin `<pinned-sha>` to a reviewed commit in this repository. Protect the caller's default branch with these two checks: **Conventional pull request title** and **Changelog updated when required**.

Titles must use one of `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, or `revert`; scope and `!` are supported. Every valid title is checked. Only `chore`, `ci`, `style`, `test`, and `revert` skip the changelog-file requirement. This v1 check only establishes that `CHANGELOG.md` changed; it does not check prose or prove an Unreleased entry was added.

The caller grants only read permissions and safely works for fork PRs. It never uses `pull_request_target` or executes PR code.

## Manual releases

Use `examples/publish-release.yml`; reusable workflows cannot supply the caller's `workflow_dispatch` form. The caller must grant `contents: write` (called workflows cannot elevate it), run on its default branch, and pass a stable, increasing `X.Y.Z` without `v`.

The workflow supports a literal `[project] version = "X.Y.Z"` in `pyproject.toml`, or a `VERSION` file for a workflow-only repository, plus `## [Unreleased]` and Keep-a-Changelog release headings. This repository enables both workflows directly: pull-request policy runs on its own PRs, and Publish release can be dispatched from Actions. The included standard-library helper is tested against semantic-version history with comparison links and date-only history without them. It does not migrate old history. It creates a `chore(release): X.Y.Z` commit, `vX.Y.Z` tag, and GitHub Release whose notes are the former Unreleased content.

The standard-library Python helper performs the changelog rollover and is checked out at `github.workflow_sha`, the same revision as this workflow, because a caller checkout is its own repository.

Release operations serialize per repository and never cancel one another. A protected default branch that rejects `GITHUB_TOKEN` writes fails safely; release-PR mode is intentionally not included. `GITHUB_TOKEN` pushes do not normally trigger push workflows, so run consumer checks before dispatching. If commit/tag publication succeeds but release creation fails, rerun only after verifying the tag points to the release commit; do not delete or move it. A matching completed release is a no-op; a conflicting tag/release requires manual recovery.

For private callers, GitHub must allow that repository to access this private workflow repository; otherwise make this repository public or configure Actions access in repository settings.

## Development

See [CONTRIBUTING.md](CONTRIBUTING.md). The single local command is:

```sh
actionlint && python3 -m unittest discover -s tests -v
```
