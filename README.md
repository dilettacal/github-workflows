# github-workflows

Shared GitHub Actions policy and release workflows, maintained once and pinned by consumer repositories.

## Workflows

| Workflow | Purpose |
| --- | --- |
| `pull-request-policy.yml` | Checks Conventional Commit-style PR titles and requires a changed `CHANGELOG.md` for releasable work. |
| `publish-release.yml` | Prepares a versioned release PR. |
| `publish-merged-release.yml` | Publishes the tag and GitHub Release when a `chore(release): X.Y.Z` PR merges. |

## Use

Copy a caller from [`examples/`](examples/), pin `<pinned-sha>`, and keep the
caller responsible for events, permissions, checks, and branch protection.

Release and publish callers pass the same SHA as `workflows-ref`: inside `workflow_call`,
`github.workflow_sha` is the caller's commit, not this repository's.

Release callers dispatch `X.Y.Z` once to open a release PR. With the
`publish-merged-release.yml` caller, merging that PR publishes the tag and
GitHub Release. Without it, dispatch the same version again after merging.

## Development

```sh
pre-commit run --all-files && actionlint && python3 -m unittest discover -s tests -v
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for setup.
