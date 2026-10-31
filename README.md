# github-workflows

Reusable GitHub Actions workflows for repositories.

## Pull Request Policy

Use `examples/pull-request-policy.yml` (pinned to a commit SHA). Requires `contents: read` and safe for forks.

Enforces:
- **PR Title**: Standard types (`feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`).
- **Changelog**: Requires `CHANGELOG.md` edits unless the type is `chore`, `ci`, `style`, `test`, or `revert`.

## Manual Releases

Use `examples/publish-release.yml` on the default branch with `contents: write`. Enter a version (`X.Y.Z`).

- Supports `pyproject.toml` (`version = "X.Y.Z"`) or a `VERSION` file, along with a `## [Unreleased]` changelog section.
- Automatically creates a release commit (`chore(release): X.Y.Z`), tags `vX.Y.Z`, and creates the GitHub Release.
- Safe to re-run on failure; skips if already released.

## Development

Run tests and linting:

```sh
pre-commit run --all-files && actionlint && python3 -m unittest discover -s tests -v
