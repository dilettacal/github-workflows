# github-workflows

Shared GitHub Actions policy and release workflows, maintained once and pinned by consumer repositories.

## Workflows

| Workflow | Purpose |
| --- | --- |
| `pull-request-policy.yml` | Checks Conventional Commit-style PR titles and requires a changed `CHANGELOG.md` for releasable work. |
| `publish-release.yml` | Prepares a versioned release PR, then publishes the tag and GitHub Release after that PR merges. |

## Use

Copy a caller from [`examples/`](examples/), pin `<pinned-sha>`, and keep the
caller responsible for events, permissions, checks, and branch protection.

Release callers pass the same SHA as `workflows-ref`: inside `workflow_call`,
`github.workflow_sha` is the caller's commit, not this repository's.

Release callers dispatch `X.Y.Z`: first run opens a release PR; after merging
it, run the same version again to publish the tag and GitHub Release.

## Development

```sh
pre-commit run --all-files && actionlint && python3 -m unittest discover -s tests -v
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for setup.
