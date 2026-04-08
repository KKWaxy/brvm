# Changelog

Tous les changements notables de ce projet seront documentés dans ce fichier.

Le format est basé sur [Keep a Changelog](https://keepachangelog.com/),
et ce projet adhère au [Semantic Versioning](https://semver.org/).

## [0.1.0] - 2026-04-08

### 🎉 Ajouté
- Implémentation API CRUD complète pour gérer les données SGI
- Import automatique des données depuis fichier CSV (38 enregistrements SGI)
- Support SQLite par défaut, configurable pour PostgreSQL/MySQL
- UUID comme clés primaires pour meilleure sécurité
- Horodatage automatique (created_at, updated_at) pour traçabilité
- 15 endpoints API:
  - `GET /sgi` - Liste avec pagination et filtres
  - `GET /sgi/count` - Compte total
  - `GET /sgi/countries` - Liste des pays uniques
  - `GET /sgi/{id}` - Détail d'un SGI
  - `POST /sgi` - Créer un SGI
  - `PATCH /sgi/{id}` - Mise à jour partielle
  - `DELETE /sgi/{id}` - Suppression
  - Et plus...
- Documentation Swagger UI et ReDoc automatique
- Validation Pydantic pour tous les inputs
- Schémas de réponse typés
- Support CORS configurable
- Base de données SQLAlchemy ORM avec migrations Alembic
- Configuration via variables d'environnement
- Logging structuré
- Type hints complets avec MyPy compliance
- Linting Ruff avec PEP 8 compliance
- Tests API automatisés
- Documentation complète:
  - README.md avec exemples d'utilisation
  - API_DOCUMENTATION.md avec tous les endpoints
  - Guide d'installation
  - Guide de contribution

### 🔒 Sécurité
- Binding serveur sécurisé (localhost par défaut)
- Debug mode désactivé par défaut
- Secrets gérés via variables d'environnement
- Protection SQL injection via ORM
- Validation complète des inputs
- Mise à jour setuptools pour fixer 5 CVEs
- Code audit complet (ruff, mypy, pip-audit)
- Rapport de sécurité (SECURITY_AUDIT.md)

### 📦 Structure du Projet
```
sgi/
├── app/
│   ├── api.py          # Factory FastAPI
│   ├── config.py       # Configuration
│   ├── database.py     # SQLAlchemy setup
│   ├── models.py       # Modèles de données
│   ├── schemas.py      # Schémas Pydantic
│   ├── loader.py       # Chargement CSV
│   └── routes.py       # Endpoints API
├── tests/              # Tests
├── data/               # Données CSV
├── main.py             # Point d'entrée
├── pyproject.toml      # Configuration projet
└── README.md           # Documentation
```

### 🛠️ Technologies
- Python 3.10+
- FastAPI 0.135.3
- SQLAlchemy 2.0.49
- Pydantic 2.12.5
- Uvicorn 0.44.0
- SQLite (PostgreSQL/MySQL supported)

### 📋 Notes
- Version initiale (alpha)
- Prête pour développement et tests
- Plus de fonctionnalités à venir

---

## Roadmap

- [ ] Authentification JWT
- [ ] Rate limiting
- [ ] Webhooks
- [ ] Batch operations API
- [ ] Export en format CSV/Excel
- [ ] Dashboard web
- [ ] Tests unitaires complets
- [ ] Documentation API OpenAPI PDF
- [ ] Docker support
- [ ] Kubernetes manifests
