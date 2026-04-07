# SGI API - Endpoints Documentation

## Overview
The SGI API provides complete CRUD operations for managing SGI (Sociétés de Gestion d'Intermédiaires) data imported from CSV.

## Base URL
```
http://localhost:8000
```

## Authentication
Currently no authentication required. 

## Response Format
All endpoints return JSON responses.

---

## Health & Status Endpoints

### Health Check
- **GET** `/health`
- Returns the health status of the API
- **Response:** `{"status": "healthy"}`

### Root Endpoint
- **GET** `/`
- Welcome message and API version
- **Response:** `{"message": "Welcome to SGI API", "version": "0.1.0"}`

---

## SGI Data Endpoints

### List All SGI
- **GET** `/sgi`
- Get paginated list of all SGI records with optional filters
- **Query Parameters:**
  - `skip`: Number of records to skip (default: 0, min: 0)
  - `limit`: Max records per page (default: 100, max: 1000)
  - `pays`: Filter by country (optional, partial match)
  - `nom`: Filter by name (optional, partial match)
- **Example:** `GET /sgi?skip=0&limit=50&pays=SÉNÉGAL`
- **Response:** Array of SGI objects with 200 status

### Count Total SGI Records
- **GET** `/sgi/count`
- Get total count of all SGI records in database
- **Response:** `{"total": 125}`

### Get All Countries
- **GET** `/sgi/countries`
- Get unique list of all countries (sorted alphabetically)
- **Response:** Array of country strings

### Get SGI by Specific Country
- **GET** `/sgi/by-country/{pays}`
- Get all SGI from a specific country
- **Path Parameters:**
  - `pays`: Country name (required)
- **Query Parameters:**
  - `skip`: Number of records to skip (default: 0)
  - `limit`: Max records per page (default: 100)
- **Example:** `GET /sgi/by-country/CÔTE%20D'IVOIRE?limit=50`
- **Response:** Array of SGI objects or 404 if country not found

### Search SGI
- **GET** `/sgi/search`
- Full-text search across name, email, and phone
- **Query Parameters:**
  - `q`: Search query (required, min length: 1)
  - `skip`: Number of records to skip (default: 0)
  - `limit`: Max records per page (default: 100)
- **Example:** `GET /sgi/search?q=ABCO&limit=25`
- **Response:** Array of matching SGI objects

### Get Single SGI by ID
- **GET** `/sgi/{sgi_id}`
- Get detailed information for a specific SGI
- **Path Parameters:**
  - `sgi_id`: SGI record ID (required, must be integer)
- **Example:** `GET /sgi/1`
- **Response:** Single SGI object or 404 if not found

### Create New SGI Record
- **POST** `/sgi`
- Create a new SGI record
- **Request Body:** SGI object with required fields (at minimum `nom`)
- **Example Request:**
  ```json
  {
    "nom": "New SGI Inc",
    "adresse": "123 Main St",
    "pays": "FRANCE",
    "email": "contact@newsgi.com",
    "telephone": "+33 1 23 45 67 89"
  }
  ```
- **Response:** Created SGI object with 201 status

### Update SGI Record (Full Update)
- **PUT** `/sgi/{sgi_id}`
- Update all fields of an existing SGI record
- **Path Parameters:**
  - `sgi_id`: SGI record ID (required)
- **Request Body:** Complete SGI object
- **Response:** Updated SGI object or 404 if not found

### Partial Update SGI Record
- **PATCH** `/sgi/{sgi_id}`
- Update only specified fields of an SGI record
- **Path Parameters:**
  - `sgi_id`: SGI record ID (required)
- **Request Body:** SGI object with only fields to update
- **Example Request:**
  ```json
  {
    "email": "newemail@test.com",
    "telephone": "+33 9 87 65 43 21"
  }
  ```
- **Response:** Updated SGI object or 404 if not found

### Delete SGI Record
- **DELETE** `/sgi/{sgi_id}`
- Delete a specific SGI record
- **Path Parameters:**
  - `sgi_id`: SGI record ID (required)
- **Response:** 204 No Content on success, 404 if not found

### Bulk Delete SGI Records
- **POST** `/sgi/bulk/delete`
- Delete multiple SGI records at once
- **Request Body:**
  ```json
  {
    "ids": [1, 2, 3, 4, 5]
  }
  ```
- **Response:** `{"deleted": 5}`

---

## SGI Data Model

```json
{
  "id": 1,
  "nom": "ABCO Bourse",
  "adresse": "Résidence Moumtazz, Avenue Cheikh Anta Diop, Mermoz - Face 2ème Porte, DAKAR - SENEGAL",
  "bp": "6956 Dakar – Etoile",
  "pays": "SÉNÉGAL",
  "email": "contact@abcobourse.com",
  "fax": "(+221) 33 822 68 01",
  "telephone": "(+221) 33 822 68 00",
  "site_web": "www.abcobourse.com",
  "agrement_crepmf": null,
  "gestion_libre": "Oui",
  "apport_initial_fcfa": "50,000",
  "courtage": "0.27% - 0.5%",
  "frais_conservation": "0 FCFA / inclus",
  "observations": "Plateforme BS Trade"
}
```

---

## Error Responses

### 400 Bad Request
Invalid query parameters or request body

### 404 Not Found
Resource not found (SGI ID, country, etc.)

### 422 Unprocessable Entity
Validation error in request payload

### 500 Internal Server Error
Server error

---

## Usage Examples

### Get all SGI from Senegal
```bash
curl "http://localhost:8000/sgi?pays=SÉNÉGAL&limit=50"
```

### Search for ABCO
```bash
curl "http://localhost:8000/sgi/search?q=ABCO"
```

### Create new SGI
```bash
curl -X POST "http://localhost:8000/sgi" \
  -H "Content-Type: application/json" \
  -d '{
    "nom": "My SGI",
    "pays": "MAURITIUS",
    "email": "contact@mysgi.com"
  }'
```

### Update SGI email
```bash
curl -X PATCH "http://localhost:8000/sgi/1" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "newemail@example.com"
  }'
```

### Get total count
```bash
curl "http://localhost:8000/sgi/count"
```

---

## Interactive Documentation

Once the server is running, visit:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

These provide interactive documentation and allow testing endpoints directly.
