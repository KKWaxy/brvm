#!/usr/bin/env python3
"""
Test script for the new Review endpoints.
"""

import requests
from uuid import UUID

BASE_URL = "http://localhost:8000"

def test_reviews():
    """Test all review endpoints."""
    print("=" * 80)
    print("Testing Review Endpoints")
    print("=" * 80)
    
    # 1. Get the first SGI to test with
    print("\n1️⃣ Getting first SGI...")
    response = requests.get(f"{BASE_URL}/sgi?limit=1")
    assert response.status_code == 200, f"Failed to get SGI: {response.text}"
    sgi_list = response.json()
    assert len(sgi_list) > 0, "No SGI found in database"
    sgi = sgi_list[0]
    sgi_id = sgi["id"]
    print(f"✅ Found SGI: {sgi['nom']} (ID: {sgi_id})")
    
    # 2. Create a review
    print("\n2️⃣ Creating a review...")
    review_data = {
        "rating": 5,
        "comment": "Excellent service de gestion! Très professionnel.",
        "reviewer_name": "Jean Dupont",
        "reviewer_email": "jean@example.com"
    }
    response = requests.post(f"{BASE_URL}/sgi/{sgi_id}/reviews", json=review_data)
    assert response.status_code == 200, f"Failed to create review: {response.text}"
    review = response.json()
    review_id = review["id"]
    print(f"✅ Created review with ID: {review_id}")
    print(f"   Rating: {review['rating']}/5")
    print(f"   Comment: {review['comment']}")
    
    # 3. Create another review
    print("\n3️⃣ Creating another review...")
    review_data2 = {
        "rating": 4,
        "comment": "Bon service, mais amélioration possible.",
        "reviewer_name": "Marie Martin",
        "reviewer_email": "marie@example.com"
    }
    response = requests.post(f"{BASE_URL}/sgi/{sgi_id}/reviews", json=review_data2)
    assert response.status_code == 200, f"Failed to create review: {response.text}"
    review2 = response.json()
    review2_id = review2["id"]
    print(f"✅ Created review with ID: {review2_id}")
    
    # 4. Get all reviews for this SGI
    print("\n4️⃣ Getting all reviews for SGI...")
    response = requests.get(f"{BASE_URL}/sgi/{sgi_id}/reviews")
    assert response.status_code == 200, f"Failed to get reviews: {response.text}"
    reviews = response.json()
    print(f"✅ Found {len(reviews)} reviews:")
    for i, r in enumerate(reviews, 1):
        print(f"   {i}. Rating: {r['rating']} ⭐ - {r['reviewer_name']}")
    
    # 5. Get a specific review
    print("\n5️⃣ Getting a specific review...")
    response = requests.get(f"{BASE_URL}/sgi/{sgi_id}/reviews/{review_id}")
    assert response.status_code == 200, f"Failed to get review: {response.text}"
    review = response.json()
    print(f"✅ Retrieved review: {review['reviewer_name']} - Rating: {review['rating']}")
    
    # 6. Update a review
    print("\n6️⃣ Updating review...")
    update_data = {
        "rating": 5,
        "comment": "Vraiment excellent service! Je recommande."
    }
    response = requests.put(f"{BASE_URL}/sgi/{sgi_id}/reviews/{review_id}", json=update_data)
    assert response.status_code == 200, f"Failed to update review: {response.text}"
    updated_review = response.json()
    print(f"✅ Updated review:")
    print(f"   New rating: {updated_review['rating']}/5")
    print(f"   New comment: {updated_review['comment']}")
    
    # 7. Get average rating
    print("\n7️⃣ Getting average rating...")
    response = requests.get(f"{BASE_URL}/sgi/{sgi_id}/rating-average")
    assert response.status_code == 200, f"Failed to get average rating: {response.text}"
    rating_data = response.json()
    print(f"✅ Average rating for {rating_data['sgi_nom']}:")
    print(f"   Average: {rating_data['average_rating']} ⭐")
    print(f"   Total reviews: {rating_data['total_reviews']}")
    
    # 8. Get SGI with reviews
    print("\n8️⃣ Getting SGI with all reviews...")
    response = requests.get(f"{BASE_URL}/sgi/{sgi_id}/with-reviews")
    assert response.status_code == 200, f"Failed to get SGI with reviews: {response.text}"
    sgi_with_reviews = response.json()
    print(f"✅ Retrieved SGI with {len(sgi_with_reviews['reviews'])} reviews:")
    print(f"   SGI: {sgi_with_reviews['nom']}")
    print(f"   Country: {sgi_with_reviews['pays']}")
    print(f"   Reviews: {len(sgi_with_reviews['reviews'])}")
    
    # 9. Delete a review
    print("\n9️⃣ Deleting a review...")
    response = requests.delete(f"{BASE_URL}/sgi/{sgi_id}/reviews/{review2_id}")
    assert response.status_code == 200, f"Failed to delete review: {response.text}"
    print(f"✅ Review deleted successfully")
    
    # 10. Verify deletion
    print("\n🔟 Verifying deletion...")
    response = requests.get(f"{BASE_URL}/sgi/{sgi_id}/reviews")
    assert response.status_code == 200, f"Failed to get reviews: {response.text}"
    reviews = response.json()
    print(f"✅ Remaining reviews: {len(reviews)}")
    
    # 11. Test validation - invalid rating
    print("\n1️⃣1️⃣ Testing validation (invalid rating)...")
    invalid_review = {
        "rating": 10,  # Invalid, must be 1-5
        "comment": "This should fail"
    }
    response = requests.post(f"{BASE_URL}/sgi/{sgi_id}/reviews", json=invalid_review)
    assert response.status_code == 400, f"Should have failed for invalid rating"
    print(f"✅ Validation works: {response.json()['detail']}")
    
    # 12. Test 404 - non-existent SGI
    print("\n1️⃣2️⃣ Testing 404 (non-existent SGI)...")
    fake_id = "00000000-0000-0000-0000-000000000000"
    response = requests.post(f"{BASE_URL}/sgi/{fake_id}/reviews", json=review_data)
    assert response.status_code == 404, f"Should have returned 404"
    print(f"✅ 404 response: {response.json()['detail']}")
    
    print("\n" + "=" * 80)
    print("✅ All tests passed! Review functionality is working correctly.")
    print("=" * 80)

if __name__ == "__main__":
    test_reviews()
