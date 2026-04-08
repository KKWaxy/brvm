# Installation Guide

This guide provides detailed instructions for installing and setting up SGI.

## Table of Contents

- [System Requirements](#system-requirements)
- [Installation Methods](#installation-methods)
- [Quick Start](#quick-start)
- [Troubleshooting](#troubleshooting)

## System Requirements

- **Python**: 3.10 or higher
- **Operating System**: Linux, macOS, or Windows
- **RAM**: Minimum 512 MB
- **Disk Space**: Minimum 100 MB for installation

## Installation Methods

### Method 1: Using UV (Recommended)

UV is a modern, fast Python package installer and resolver.

1. **Install UV** (if not already installed):
   ```bash
   pip install uv
   ```

2. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/sgi.git
   cd sgi
   ```

3. **Install dependencies**:
   ```bash
   uv sync
   ```

4. **Activate the virtual environment**:
   ```bash
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

### Method 2: Using Pip and Venv

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/sgi.git
   cd sgi
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv .venv
   ```

3. **Activate the virtual environment**:
   ```bash
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

4. **Install dependencies**:
   ```bash
   pip install --upgrade pip setuptools wheel
   pip install -e .
   ```

### Method 3: Docker (Coming Soon)

Docker support is planned for future releases.

## Quick Start

### 1. Configuration

Create a `.env` file in the project root (or use the existing `.env.example`):

```bash
cp .env.example .env
```

Edit `.env` with your configuration:

```env
APP_NAME=SGI
APP_VERSION=0.1.0
DEBUG=false
DATABASE_URL=sqlite:///./app.db
SERVER_HOST=127.0.0.1
SERVER_PORT=8000
```

### 2. Database Setup

The database is automatically initialized on first run. To manually initialize:

```bash
python -c "from app.database import init_db; init_db()"
```

### 3. Run the Server

```bash
python -m uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

### 4. Access Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### 5. Test the API

```bash
python test_api_endpoints.py
```

## Configuration

### Environment Variables

Create a `.env` file with the following variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `APP_NAME` | SGI | Application name |
| `APP_VERSION` | 0.1.0 | Application version |
| `DEBUG` | false | Enable debug mode |
| `DATABASE_URL` | sqlite:///./app.db | Database URL |
| `SERVER_HOST` | 127.0.0.1 | Server host (localhost for security) |
| `SERVER_PORT` | 8000 | Server port |

### Database Configuration

#### SQLite (Default)

```env
DATABASE_URL=sqlite:///./app.db
```

SQLite is perfect for development and small deployments.

#### PostgreSQL

```bash
pip install psycopg2-binary
```

```env
DATABASE_URL=postgresql://user:password@localhost:5432/sgi_db
```

#### MySQL

```bash
pip install pymysql
```

```env
DATABASE_URL=mysql+pymysql://user:password@localhost:3306/sgi_db
```

## Development Setup

### Install Development Dependencies

```bash
pip install -e ".[dev]"
```

Or with UV:

```bash
uv sync --all-extras
```

### Run Tests

```bash
pytest tests/ -v
```

### Code Quality Checks

```bash
# Linting
ruff check app/ main.py

# Code formatting
ruff format app/ main.py

# Type checking
mypy app/ main.py

# Security audit
pip-audit
```

### Pre-commit Hooks (Optional)

Set up pre-commit hooks to automatically run checks:

1. **Install pre-commit**:
   ```bash
   pip install pre-commit
   ```

2. **Create `.pre-commit-config.yaml`** (optional):
   ```yaml
   repos:
     - repo: https://github.com/astral-sh/ruff-pre-commit
       rev: v0.1.0
       hooks:
         - id: ruff
         - id: ruff-format
   ```

3. **Install the hooks**:
   ```bash
   pre-commit install
   ```

## Troubleshooting

### Python Version Issues

If you get `python: command not found`, try:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Then use `python` or `python3` consistently.

### Permission Denied Errors

On Linux/macOS, if you get permission errors:

```bash
chmod +x .venv/bin/activate
source .venv/bin/activate
```

### Database Errors

**SQLite database locked**:
- Close other connections to the database
- Make sure only one Uvicorn process is running

**PostgreSQL connection error**:
- Check PostgreSQL is running: `psql --version`
- Verify connection string in `.env`
- Check user permissions: `psql -U username -d sgi_db`

### Import Errors

If you get import errors:

1. Make sure you're in the virtual environment:
   ```bash
   which python  # Should show .venv path
   ```

2. Reinstall dependencies:
   ```bash
   pip install --force-reinstall -e .
   ```

### Port Already in Use

If port 8000 is already in use:

```bash
# Option 1: Use a different port
python -m uvicorn main:app --reload --port 8001

# Option 2: Kill the process using port 8000
# On Linux/macOS:
lsof -ti:8000 | xargs kill -9

# On Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Missing Dependencies

If you get `ModuleNotFoundError`:

```bash
# Reinstall everything
pip install --upgrade pip
pip install -e .
pip install -e ".[dev]"  # For development
```

## Updating

### Updating Dependencies

```bash
# With UV
uv sync --upgrade

# With pip
pip install --upgrade -r requirements.txt
```

### Updating the Application

```bash
git pull origin main
# Then reinstall if dependencies changed
pip install -e .
```

## Uninstall

To completely uninstall SGI:

```bash
# Deactivate virtual environment
deactivate

# Remove virtual environment
rm -rf .venv  # On Windows: rmdir /s /q .venv

# Remove project directory (optional)
cd ..
rm -rf sgi
```

## Next Steps

- Read the [README.md](../README.md) for an overview
- Check [API_DOCUMENTATION.md](../API_DOCUMENTATION.md) for API endpoints
- See [CONTRIBUTING.md](../CONTRIBUTING.md) to contribute
- Review [SECURITY_AUDIT.md](../SECURITY_AUDIT.md) for security info

## Getting Help

- 📖 [Documentation](../README.md)
- 🐛 [Report Issues](https://github.com/yourusername/sgi/issues)
- 💬 [Discussions](https://github.com/yourusername/sgi/discussions)
- 📧 [Email](mailto:contact@example.com)

## License

This project is licensed under the MIT License. See [LICENSE](../LICENSE) for details.
