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

## Review & Rating Endpoints

### List Reviews for an SGI
- **GET** `/sgi/{sgi_id}/reviews`
- Get all reviews for a specific SGI with pagination
- **Path Parameters:**
  - `sgi_id`: UUID of the SGI (required)
- **Query Parameters:**
  - `skip`: Number of records to skip (default: 0, min: 0)
  - `limit`: Max records per page (default: 100, max: 1000)
- **Response:** Array of Review objects
- **Example Response:**
  ```json
  [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "sgi_id": "550e8400-e29b-41d4-a716-446655440001",
      "rating": 5,
      "comment": "Excellent service!",
      "reviewer_name": "Jean Dupont",
      "reviewer_email": "jean@example.com",
      "created_at": "2024-01-15T10:30:00",
      "updated_at": "2024-01-15T10:30:00"
    }
  ]
  ```

### Get Specific Review
- **GET** `/sgi/{sgi_id}/reviews/{review_id}`
- Get a specific review by its ID
- **Path Parameters:**
  - `sgi_id`: UUID of the SGI (required)
  - `review_id`: UUID of the review (required)
- **Response:** Single Review object with 200 status or 404 if not found

### Create Review
- **POST** `/sgi/{sgi_id}/reviews`
- Create a new review for an SGI with rating (1-5 stars) and optional comment
- **Path Parameters:**
  - `sgi_id`: UUID of the SGI (required)
- **Request Body:**
  ```json
  {
    "rating": 5,
    "comment": "Excellent service de gestion!",
    "reviewer_name": "Marie Martin",
    "reviewer_email": "marie@example.com"
  }
  ```
- **Validation:**
  - `rating`: Integer between 1 and 5 (required) ⭐⭐⭐⭐⭐
  - `comment`: String (optional)
  - `reviewer_name`: String (optional)
  - `reviewer_email`: String (optional)
- **Response:** Created Review object with 200 status
- **Errors:**
  - 400: Invalid rating (must be between 1-5)
  - 404: SGI not found

### Update Review
- **PUT** `/sgi/{sgi_id}/reviews/{review_id}`
- Update an existing review (all fields optional)
- **Path Parameters:**
  - `sgi_id`: UUID of the SGI (required)
  - `review_id`: UUID of the review (required)
- **Request Body:** (All fields optional)
  ```json
  {
    "rating": 4,
    "comment": "Good service, but could improve",
    "reviewer_name": "Updated Name",
    "reviewer_email": "updated@example.com"
  }
  ```
- **Response:** Updated Review object with 200 status
- **Errors:**
  - 400: Invalid rating (must be between 1-5)
  - 404: Review not found

### Delete Review
- **DELETE** `/sgi/{sgi_id}/reviews/{review_id}`
- Delete a review permanently
- **Path Parameters:**
  - `sgi_id`: UUID of the SGI (required)
  - `review_id`: UUID of the review (required)
- **Response:** `{"message": "Review deleted successfully"}` with 200 status
- **Errors:**
  - 404: Review not found

### Get Average Rating
- **GET** `/sgi/{sgi_id}/rating-average`
- Get the average rating and review count for a specific SGI
- **Path Parameters:**
  - `sgi_id`: UUID of the SGI (required)
- **Response:**
  ```json
  {
    "sgi_id": "550e8400-e29b-41d4-a716-446655440000",
    "sgi_nom": "ABCO Bourse",
    "average_rating": 4.5,
    "total_reviews": 2
  }
  ```
- **Note:** Returns `average_rating: null` and `total_reviews: 0` if no reviews exist

### Get SGI with All Reviews
- **GET** `/sgi/{sgi_id}/with-reviews`
- Get a specific SGI with all its associated reviews
- **Path Parameters:**
  - `sgi_id`: UUID of the SGI (required)
- **Response:** SGI object with nested `reviews` array containing all Review objects
- **Example Response:**
  ```json
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "nom": "ABCO Bourse",
    "adresse": "123 Rue de Paris",
    "pays": "SÉNÉGAL",
    "email": "contact@abco.com",
    "created_at": "2024-01-01T08:00:00",
    "updated_at": "2024-01-15T10:30:00",
    "reviews": [
      {
        "id": "550e8400-e29b-41d4-a716-446655440001",
        "sgi_id": "550e8400-e29b-41d4-a716-446655440000",
        "rating": 5,
        "comment": "Excellent!",
        "reviewer_name": "Jean Dupont",
        "reviewer_email": "jean@example.com",
        "created_at": "2024-01-15T10:30:00",
        "updated_at": "2024-01-15T10:30:00"
      }
    ]
  }
  ```
- **Errors:**
  - 404: SGI not found

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

### Create a review (5-star rating)
```bash
curl -X POST "http://localhost:8000/sgi/550e8400-e29b-41d4-a716-446655440000/reviews" \
  -H "Content-Type: application/json" \
  -d '{
    "rating": 5,
    "comment": "Excellent service de gestion!",
    "reviewer_name": "Jean Dupont",
    "reviewer_email": "jean@example.com"
  }'
```

### Get all reviews for an SGI
```bash
curl "http://localhost:8000/sgi/550e8400-e29b-41d4-a716-446655440000/reviews?limit=10"
```

### Get average rating for an SGI
```bash
curl "http://localhost:8000/sgi/550e8400-e29b-41d4-a716-446655440000/rating-average"
```

### Get SGI with all its reviews
```bash
curl "http://localhost:8000/sgi/550e8400-e29b-41d4-a716-446655440000/with-reviews"
```

### Update a review
```bash
curl -X PUT "http://localhost:8000/sgi/550e8400-e29b-41d4-a716-446655440000/reviews/550e8400-e29b-41d4-a716-446655440001" \
  -H "Content-Type: application/json" \
  -d '{
    "rating": 4,
    "comment": "Good service, could improve"
  }'
```

### Delete a review
```bash
curl -X DELETE "http://localhost:8000/sgi/550e8400-e29b-41d4-a716-446655440000/reviews/550e8400-e29b-41d4-a716-446655440001"
```

---

## Interactive Documentation

Once the server is running, visit:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

These provide interactive documentation and allow testing endpoints directly.
