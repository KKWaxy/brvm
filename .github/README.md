# GitHub Configuration

This directory contains GitHub-specific configuration files.

## Directories

- **ISSUE_TEMPLATE/** - Issue templates for bug reports and feature requests
- **workflows/** - GitHub Actions CI/CD workflows

## Workflows

### tests.yml
Runs automatically on push and pull requests:
- Unit tests (Python 3.10, 3.11, 3.12)
- Code linting with ruff
- Type checking with mypy
- Security audit with pip-audit
- Coverage reporting to Codecov

## Issue Templates

- **bug_report.md** - For reporting bugs
- **feature_request.md** - For requesting new features
- **config.yml** - Configuration for the issue tracker

## Pull Request Template

- **PULL_REQUEST_TEMPLATE.md** - Template for creating pull requests
