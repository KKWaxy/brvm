# SGI - FastAPI Application

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/fastapi-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![SQLAlchemy](https://img.shields.io/badge/sqlalchemy-2.0+-orange.svg)](https://www.sqlalchemy.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Type: mypy](https://img.shields.io/badge/type%20checking-mypy-green)](http://mypy-lang.org/)

Application FastAPI moderne pour gérer les données des Sociétés de Gestion d'Intermédiaires (SGI) avec support SQLite/PostgreSQL.

## Caractéristiques

✅ **FastAPI** - Framework web moderne et performant  
✅ **SQLAlchemy** - ORM pour la gestion de base de données  
✅ **SQLite** - Base de données intégrée (configurable)  
✅ **Import CSV** - Chargement automatique des données depuis fichier CSV  
✅ **API CRUD Complète** - Endpoints pour créer, lire, mettre à jour, supprimer les données  
✅ **Recherche et Filtrage** - Recherche textuelle et filtrage par pays  
✅ **Documentation Interactive** - Swagger UI et ReDoc  
✅ **Uv Package Manager** - Gestion moderne des dépendances  

## Prérequis

- Python 3.10+
- [uv](https://docs.astral.sh/uv/) (optionnel)

## Installation

### Avec `uv`

```bash
# Installation des dépendances
uv sync

# Activation de l'environnement virtuel
source .venv/bin/activate
```

### Avec pip

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Démarrage du serveur

### Mode développement (avec rechargement automatique)

```bash
python -m uvicorn main:app --reload
```

### Mode production

```bash
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

Le serveur sera disponible à `http://localhost:8000`

## Documentation API

Accédez à la documentation interactive une fois le serveur lancé :

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Fichier API_DOCUMENTATION.md**: Documentation complète des endpoints

## Structure du projet

```
.
├── main.py                      # Point d'entrée de l'application
├── pyproject.toml              # Configuration du projet (dépendances, etc.)
├── app/
│   ├── __init__.py
│   ├── api.py                  # Création et configuration de l'app FastAPI
│   ├── config.py               # Configuration (variables d'environnement)
│   ├── database.py             # Configuration SQLAlchemy et sessions
│   ├── models.py               # Modèles de données SQLAlchemy
│   ├── schemas.py              # Schémas Pydantic (validation)
│   ├── loader.py               # Chargeur de données CSV
│   └── routes.py               # Endpoints API
├── data/
│   └── brvm_sgi - brvm_sgi.csv # Données SGI (chargées automatiquement)
├── tests/
│   ├── __init__.py
│   └── test_api.py             # Tests unitaires
├── API_DOCUMENTATION.md         # Documentation détaillée des endpoints
└── test_api_endpoints.py       # Script de test simple des endpoints
```

## Configuration

### Variables d'environnement (.env)

```env
# Configuration de l'application
APP_NAME=SGI
APP_VERSION=0.1.0
DEBUG=false

# Configuration de la base de données
# SQLite (défaut): sqlite:///./app.db
# PostgreSQL: postgresql://user:password@localhost:5432/dbname
DATABASE_URL=sqlite:///./app.db

# Configuration du serveur (sécurité : restreint à localhost par défaut)
# Pour production avec load balancer, utiliser 0.0.0.0
SERVER_HOST=127.0.0.1
SERVER_PORT=8000
```

## Usage

### Endpoints disponibles

#### Lecture de données

```bash
# Liste de tous les SGI
curl http://localhost:8000/sgi

# Nombre total de SGI
curl http://localhost:8000/sgi/count

# Tous les pays disponibles
curl http://localhost:8000/sgi/countries

# SGI d'un pays spécifique
curl http://localhost:8000/sgi/by-country/SÉNÉGAL

# Recherche textuelle
curl http://localhost:8000/sgi/search?q=ABCO

# Un SGI par ID
curl http://localhost:8000/sgi/1
```

#### Création de données

```bash
# Créer un nouveau SGI
curl -X POST http://localhost:8000/sgi \
  -H "Content-Type: application/json" \
  -d '{
    "nom": "My SGI Inc",
    "pays": "FRANCE",
    "email": "contact@mysgi.com"
  }'
```

#### Modification de données

```bash
# Mettre à jour complètement un SGI
curl -X PUT http://localhost:8000/sgi/1 \
  -H "Content-Type: application/json" \
  -d '{"nom": "Updated Name", ...}'

# Mettre à jour partiellement
curl -X PATCH http://localhost:8000/sgi/1 \
  -H "Content-Type: application/json" \
  -d '{"email": "newemail@example.com"}'
```

#### Suppression de données

```bash
# Supprimer un SGI
curl -X DELETE http://localhost:8000/sgi/1

# Supprimer plusieurs SGI
curl -X POST http://localhost:8000/sgi/bulk/delete \
  -H "Content-Type: application/json" \
  -d '{"ids": [1, 2, 3]}'
```

## Tests

### Test automatisé

```bash
# Installer les dépendances de test
pip install pytest pytest-asyncio httpx

# Exécuter les tests
pytest tests/

# Ou avec le script de test en ligne
python test_api_endpoints.py
```

### Test manuel

Une fois le serveur lancé, visitez :
- http://localhost:8000/docs (Swagger UI)
- http://localhost:8000/redoc (ReDoc)

## Importation des données CSV

Les données sont automatiquement importées au démarrage de l'application à partir du fichier `data/brvm_sgi - brvm_sgi.csv`.

Pour réimporter les données :

```bash
# 1. Supprimer la base de données
rm app.db

# 2. Relancer le serveur
python -m uvicorn main:app --reload
```

## Modèle de données

### SGI

```json
{
  "id": 1,
  "nom": "ABCO Bourse",
  "adresse": "Résidence Moumtazz, ...",
  "bp": "6956 Dakar – Etoile",
  "pays": "SÉNÉGAL",
  "email": "contact@abcobourse.com",
  "fax": "(+221) 33 822 68 01",
  "telephone": "(+221) 33 822 68 00",
  "site_web": "www.abcobourse.com",
  "agrement_crepmf": "",
  "gestion_libre": "Oui",
  "apport_initial_fcfa": "50,000",
  "courtage": "0.27% - 0.5%",
  "frais_conservation": "0 FCFA / inclus",
  "observations": "Plateforme BS Trade"
}
```

## Dépendances principales

- **FastAPI** >= 0.104.0 - Framework web
- **Uvicorn** >= 0.24.0 - Serveur ASGI
- **SQLAlchemy** >= 2.0.0 - ORM de base de données
- **Pydantic** >= 2.0.0 - Validation de données
- **Pydantic-Settings** >= 2.0.0 - Gestion de configuration

## Dépendances de développement

- **Pytest** >= 7.4.0 - Framework de test
- **Pytest-asyncio** >= 0.21.0 - Support async pour Pytest
- **Httpx** >= 0.24.0 - Client HTTP pour tests
- **Black** >= 23.0.0 - Formatage de code
- **Ruff** >= 0.1.0 - Linter Python
- **Mypy** >= 1.5.0 - Vérification de types

## Support des bases de données

### SQLite (défaut)

```env
DATABASE_URL=sqlite:///./app.db
```

### PostgreSQL

```env
DATABASE_URL=postgresql://user:password@localhost:5432/database_name
```

À utiliser avec le driver : `pip install psycopg2-binary`

### MySQL

```env
DATABASE_URL=mysql+pymysql://user:password@localhost:3306/database_name
```

À utiliser avec le driver : `pip install pymysql`

## Performance

- **Pagination** automatique (max 1000 records par requête)
- **Filtrage** côté serveur (recherche, pays, etc.)
- **Index** sur les colonnes fréquemment consultées
- **Connection pooling** pour les requêtes rapides

## Licence

Propriétaire

## Support

Pour toute question ou problème : voir la documentation API complète en ligne.

## Structure du projet

```
sgi/
├── app/
│   ├── __init__.py
│   ├── api.py              # Factory FastAPI
│   ├── config.py           # Configuration
│   └── routes.py           # Routes API
├── tests/                  # Tests unitaires
├── main.py                 # Point d'entrée
├── pyproject.toml          # Configuration du projet
├── README.md               # Documentation
├── .gitignore              # Fichiers à ignorer
└── .env.example            # Variables d'environnement (exemple)
```

## Développement

### Lancer les tests

```bash
uv run pytest
```

### Formater le code

```bash
uv run black app/
```

### Linter

```bash
uv run ruff check app/
```

### Type checking

```bash
uv run mypy app/
```

## Configuration

Créez un fichier `.env` à la racine du projet :

```env
APP_NAME=SGI
APP_VERSION=0.1.0
DEBUG=true
```

## Licence

MIT
