# Publishing to PyPI

This guide explains how to publish SGI to the Python Package Index (PyPI).

## Prerequisites

- `build` package: `pip install build`
- `twine` package: `pip install twine`
- PyPI account: Create one at https://pypi.org/account/register/
- PyPI API token: Generate at https://pypi.org/manage/account/

## Step 1: Update Version

Update the version in `pyproject.toml`:

```toml
[project]
version = "0.1.0"  # Increment this
```

Also update in `app/config.py` if needed.

## Step 2: Build the Package

```bash
python -m build
```

This creates:
- `dist/sgi-0.1.0.tar.gz` (source distribution)
- `dist/sgi-0.1.0-py3-none-any.whl` (wheel distribution)

## Step 3: Upload to PyPI

### Using Twine (Recommended)

```bash
# Test upload first (Test PyPI)
python -m twine upload --repository testpypi dist/*

# Production upload
python -m twine upload dist/*
```

When prompted, use:
- **Username**: `__token__`
- **Password**: Your PyPI API token (starts with `pypi-`)

### Configure Credentials (Optional)

Create `~/.pypirc`:

```ini
[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-xxxxx...

[pypi]
repository = https://upload.pypi.org/legacy/
username = __token__
password = pypi-xxxxx...
```

Then upload with:
```bash
python -m twine upload dist/*
```

## Step 4: Verify Publication

Visit: https://pypi.org/project/sgi/

Or test installation:
```bash
pip install sgi
```

## Continuous Deployment (Optional)

Create `.github/workflows/publish.yml` for automatic PyPI uploads on release:

```yaml
name: Publish to PyPI

on:
  release:
    types: [created]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      
      - name: Build package
        run: |
          pip install build
          python -m build
      
      - name: Publish to PyPI
        uses: pypa/gh-action-pypi-publish@release/v1
        with:
          password: ${{ secrets.PYPI_API_TOKEN }}
```

## Release Checklist

Before publishing:

- [ ] Update `CHANGELOG.md` with new version
- [ ] Update version in `pyproject.toml`
- [ ] All tests pass: `pytest tests/`
- [ ] All checks pass: `ruff check`, `mypy`, `pip-audit`
- [ ] Clean build: `rm -rf build dist *.egg-info && python -m build`
- [ ] Commit and push changes
- [ ] Create git tag: `git tag v0.1.0 && git push origin v0.1.0`
- [ ] Create GitHub release (optional)
- [ ] Upload to PyPI

## Semantic Versioning

Follow [Semantic Versioning](https://semver.org/):

- **MAJOR.MINOR.PATCH** (e.g., 1.2.3)
- **MAJOR**: Incompatible API changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

Examples:
- `0.1.0` → `0.1.1` (bug fix)
- `0.1.0` → `0.2.0` (new feature)
- `0.2.0` → `1.0.0` (breaking changes)

## Common Issues

### 400 Bad Filename

Usually means version format is wrong. Ensure:
- No underscores in version: `0.1.0` not `0_1_0`
- No pre-release suffixes: `0.1.0a1` not `0.1.0alpha1`

### 403 Forbidden

Check:
- API token is valid
- Token hasn't expired
- Username is `__token__` (not your username)

### Upload Already Exists

You can't upload the same version twice. Either:
- Increment version
- Delete on PyPI (requires PyPI permissions)
- Use different pre-release version

## After Publishing

1. Users can install with:
   ```bash
   pip install sgi
   ```

2. Create GitHub releases linking to PyPI
3. Announce on social media, forums, etc.
4. Update project website if available

## Additional Resources

- [Python Packaging Guide](https://packaging.python.org/)
- [Twine Documentation](https://twine.readthedocs.io/)
- [PyPI Help](https://pypi.org/help/)
- [Semantic Versioning](https://semver.org/)
