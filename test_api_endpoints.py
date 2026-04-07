#!/usr/bin/env python
"""
Simple test script for SGI API endpoints.
Run this after starting the server: python test_api_endpoints.py
"""

import requests
import json

BASE_URL = "http://localhost:8000"


def print_response(title, response):
    """Pretty print API response."""
    print(f"\n{'='*60}")
    print(f"✓ {title}")
    print(f"{'='*60}")
    print(f"Status: {response.status_code}")
    try:
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    except:
        print(response.text)


def test_health():
    """Test health endpoint."""
    resp = requests.get(f"{BASE_URL}/health")
    print_response("Health Check", resp)


def test_count():
    """Test count endpoint."""
    resp = requests.get(f"{BASE_URL}/sgi/count")
    print_response("Total SGI Count", resp)


def test_countries():
    """Test get countries endpoint."""
    resp = requests.get(f"{BASE_URL}/sgi/countries")
    print_response("Get All Countries", resp)


def test_list_sgi():
    """Test list all SGI with pagination."""
    resp = requests.get(f"{BASE_URL}/sgi?skip=0&limit=2")
    print_response("List SGI (first 2)", resp)


def test_get_by_country():
    """Test get SGI by country."""
    resp = requests.get(f"{BASE_URL}/sgi/by-country/SÉNÉGAL?limit=2")
    print_response("Get SGI from SÉNÉGAL", resp)


def test_search():
    """Test search endpoint."""
    resp = requests.get(f"{BASE_URL}/sgi/search?q=ABCO")
    print_response("Search for ABCO", resp)


def test_get_single(sgi_id=None):
    """Test get single SGI by ID."""
    # Use a fetched ID if provided, otherwise get the first one
    if sgi_id:
        resp = requests.get(f"{BASE_URL}/sgi/{sgi_id}")
        print_response(f"Get SGI by ID ({sgi_id})", resp)
    else:
        # Fetch first SGI to get its ID
        resp = requests.get(f"{BASE_URL}/sgi?skip=0&limit=1")
        if resp.status_code == 200 and len(resp.json()) > 0:
            first_id = resp.json()[0]["id"]
            resp = requests.get(f"{BASE_URL}/sgi/{first_id}")
            print_response(f"Get SGI by ID ({first_id})", resp)


def test_create():
    """Test create new SGI."""
    payload = {
        "nom": "Test SGI Ltd",
        "pays": "TEST",
        "email": "test@example.com",
        "telephone": "+1 234 567 890",
    }
    resp = requests.post(f"{BASE_URL}/sgi", json=payload)
    print_response("Create New SGI", resp)
    return resp.json()["id"] if resp.status_code == 201 else None


def test_update(sgi_id):
    """Test update SGI."""
    payload = {
        "email": "updated@example.com",
        "telephone": "+1 987 654 321",
    }
    resp = requests.patch(f"{BASE_URL}/sgi/{sgi_id}", json=payload)
    print_response(f"Update SGI (ID: {sgi_id})", resp)


def test_delete(sgi_id):
    """Test delete SGI."""
    resp = requests.delete(f"{BASE_URL}/sgi/{sgi_id}")
    print_response(f"Delete SGI (ID: {sgi_id})", resp)
    print(f"Response status: {resp.status_code}")


def main():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("SGI API Endpoint Tests")
    print("=" * 60)

    try:
        # Health checks
        test_health()

        # Data retrieval tests
        test_count()
        test_countries()
        test_list_sgi()
        test_get_by_country()
        test_search()
        test_get_single()

        # CRUD tests
        print("\n" + "=" * 60)
        print("Testing CRUD Operations")
        print("=" * 60)

        created_id = test_create()
        if created_id:
            print(f"\n✓ Created SGI with ID: {created_id}")
            test_update(created_id)
            test_delete(created_id)

        print("\n" + "=" * 60)
        print("✓ All tests completed!")
        print("=" * 60)

    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Cannot connect to server at", BASE_URL)
        print("Make sure the server is running: python -m uvicorn main:app --reload")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")


if __name__ == "__main__":
    main()
