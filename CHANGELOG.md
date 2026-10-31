# Changelog

All notable changes to these reusable GitHub Actions workflows are recorded here.

## [Unreleased]

## [0.1.1] - 2026-10-31

### Fixed

- Check out release scripts at the caller-pinned `workflows-ref`; `github.workflow_sha` is the caller's commit under `workflow_call`.
- Grant `pull-requests: write` in the release caller example.

## [0.1.0] - 2026-10-31

### Added

- Reusable pull request policy and manual release workflows.

### Fixed

- Prepare releases through a pull request before publishing their tag and GitHub Release.
- Publish the tag and GitHub Release automatically when a release PR merges.
