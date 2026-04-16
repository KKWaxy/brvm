"""Tests for review moderation endpoints."""

import pytest
import os
from uuid import uuid4
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool
import sys

# Set test mode before importing app modules
os.environ["TESTING"] = "true"

from app.api import create_app
from app.auth import hash_password
from app.database import get_db, Base
from app.enums import ReviewStatus
from app.models import User, SGI, Review
from datetime import datetime


@pytest.fixture(scope="function")
def db_engine():
    """Create an in-memory database engine for tests."""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool  # Use StaticPool to keep a single connection
    )
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    yield engine
    
    # Clean up
    engine.dispose()


@pytest.fixture(scope="function")
def db_session(db_engine):
    """Create a test database session."""
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)
    session = TestingSessionLocal()

    yield session

    session.close()


@pytest.fixture(scope="function")
def client(db_engine, db_session):
    """Create a test client with dependency override."""
    # Create the app
    app = create_app()
    
    # Override the database dependency
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    
    # Create test client
    client = TestClient(app)
    
    yield client
    
    # Clean up
    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def admin_user(db_session):
    """Create an admin user for testing."""
    user = User(
        id=uuid4(),
        email="admin@example.com",
        username="admin",
        hashed_password=hash_password("password123"),
        full_name="Admin User",
        is_active=True,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture(scope="function")
def regular_user(db_session):
    """Create a regular user for testing."""
    user = User(
        id=uuid4(),
        email="user@example.com",
        username="testuser",
        hashed_password=hash_password("password123"),
        full_name="Test User",
        is_active=True,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture(scope="function")
def sgi(db_session):
    """Create a test SGI."""
    sgi_item = SGI(
        id=uuid4(),
        nom="Test SGI",
        adresse="123 Test Street",
        pays="Test Country",
        email="sgi@example.com",
    )
    db_session.add(sgi_item)
    db_session.commit()
    db_session.refresh(sgi_item)
    return sgi_item


@pytest.fixture(scope="function")
def pending_review(db_session, sgi, regular_user):
    """Create a pending review."""
    review = Review(
        id=uuid4(),
        sgi_id=sgi.id,
        user_id=regular_user.id,
        rating=5,
        comment="Excellent service",
        reviewer_name="John Doe",
        reviewer_email="john@example.com",
        status=ReviewStatus.PENDING,
    )
    db_session.add(review)
    db_session.commit()
    db_session.refresh(review)
    return review


@pytest.fixture(scope="function")
def approved_review(db_session, sgi, regular_user, admin_user):
    """Create an approved review."""
    review = Review(
        id=uuid4(),
        sgi_id=sgi.id,
        user_id=regular_user.id,
        rating=4,
        comment="Good service",
        reviewer_name="Jane Doe",
        reviewer_email="jane@example.com",
        status=ReviewStatus.APPROVED,
        moderated_by=admin_user.id,
        moderated_at=datetime.utcnow(),
    )
    db_session.add(review)
    db_session.commit()
    db_session.refresh(review)
    return review


def get_admin_token(client, admin_user):
    """Get JWT token for admin user."""
    response = client.post(
        "/auth/login",
        json={"email": "admin@example.com", "password": "password123"},
    )
    return response.json()["access_token"]


def get_user_token(client, regular_user):
    """Get JWT token for regular user."""
    response = client.post(
        "/auth/login",
        json={"email": "user@example.com", "password": "password123"},
    )
    return response.json()["access_token"]


class TestListPendingReviews:
    """Test listing pending reviews."""

    def test_list_pending_reviews_success(self, client, admin_user, pending_review):
        """Test successful listing of pending reviews."""
        token = get_admin_token(client, admin_user)
        
        response = client.get(
            "/admin/reviews/pending",
            headers={"Authorization": f"Bearer {token}"},
        )
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1
        assert any(r["id"] == str(pending_review.id) for r in data)

    def test_list_pending_reviews_no_auth(self, client, pending_review):
        """Test listing pending reviews without authentication."""
        response = client.get("/admin/reviews/pending")
        
        # FastAPI HTTPBearer returns 403 when no credentials provided
        assert response.status_code in [401, 403]

    def test_list_pending_reviews_excludes_approved(
        self, client, admin_user, pending_review, approved_review
    ):
        """Test that approved reviews are excluded from list."""
        token = get_admin_token(client, admin_user)
        
        response = client.get(
            "/admin/reviews/pending",
            headers={"Authorization": f"Bearer {token}"},
        )
        
        assert response.status_code == 200
        data = response.json()
        assert not any(r["id"] == str(approved_review.id) for r in data)

    def test_list_pending_reviews_pagination(
        self, client, admin_user, db_session, sgi
    ):
        """Test pagination of pending reviews."""
        token = get_admin_token(client, admin_user)
        
        # Create multiple pending reviews
        for i in range(5):
            review = Review(
                id=uuid4(),
                sgi_id=sgi.id,
                rating=4,
                comment=f"Review {i}",
                reviewer_name=f"User {i}",
                reviewer_email=f"user{i}@example.com",
                status=ReviewStatus.PENDING,
            )
            db_session.add(review)
        db_session.commit()
        
        response = client.get(
            "/admin/reviews/pending?skip=0&limit=2",
            headers={"Authorization": f"Bearer {token}"},
        )
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) <= 2


class TestApproveReview:
    """Test approving reviews."""

    def test_approve_review_success(self, client, admin_user, pending_review):
        """Test successful approval of a review."""
        token = get_admin_token(client, admin_user)
        
        response = client.put(
            f"/admin/reviews/{pending_review.id}/approve",
            json={"moderation_reason": "Legit and helpful review"},
            headers={"Authorization": f"Bearer {token}"},
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == ReviewStatus.APPROVED
        assert data["moderation_reason"] == "Legit and helpful review"
        assert data["moderated_by"] == str(admin_user.id)

    def test_approve_review_no_auth(self, client, pending_review):
        """Test approving review without authentication."""
        response = client.put(
            f"/admin/reviews/{pending_review.id}/approve",
            json={"moderation_reason": "Legit review"},
        )
        
        assert response.status_code in [401, 403]

    def test_approve_nonexistent_review(self, client, admin_user):
        """Test approving a nonexistent review."""
        token = get_admin_token(client, admin_user)
        fake_id = uuid4()
        
        response = client.put(
            f"/admin/reviews/{fake_id}/approve",
            json={"moderation_reason": "Legit review"},
            headers={"Authorization": f"Bearer {token}"},
        )
        
        assert response.status_code == 404
        assert "Review not found" in response.json()["detail"]

    def test_approve_already_approved_review(
        self, client, admin_user, approved_review
    ):
        """Test approving an already approved review."""
        token = get_admin_token(client, admin_user)
        
        response = client.put(
            f"/admin/reviews/{approved_review.id}/approve",
            json={"moderation_reason": "Another reason"},
            headers={"Authorization": f"Bearer {token}"},
        )
        
        assert response.status_code == 400
        assert "not pending" in response.json()["detail"]

    def test_approve_with_optional_reason(self, client, admin_user, pending_review):
        """Test approving review with optional reason."""
        token = get_admin_token(client, admin_user)
        
        response = client.put(
            f"/admin/reviews/{pending_review.id}/approve",
            json={},
            headers={"Authorization": f"Bearer {token}"},
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == ReviewStatus.APPROVED


class TestRejectReview:
    """Test rejecting reviews."""

    def test_reject_review_success(self, client, admin_user, pending_review):
        """Test successful rejection of a review."""
        token = get_admin_token(client, admin_user)
        
        response = client.put(
            f"/admin/reviews/{pending_review.id}/reject",
            json={"moderation_reason": "Inappropriate content"},
            headers={"Authorization": f"Bearer {token}"},
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == ReviewStatus.REJECTED
        assert data["moderation_reason"] == "Inappropriate content"
        assert data["moderated_by"] == str(admin_user.id)

    def test_reject_review_no_auth(self, client, pending_review):
        """Test rejecting review without authentication."""
        response = client.put(
            f"/admin/reviews/{pending_review.id}/reject",
            json={"moderation_reason": "Bad review"},
        )
        
        assert response.status_code in [401, 403]

    def test_reject_review_missing_reason(self, client, admin_user, pending_review):
        """Test rejecting review without required reason."""
        token = get_admin_token(client, admin_user)
        
        response = client.put(
            f"/admin/reviews/{pending_review.id}/reject",
            json={},
            headers={"Authorization": f"Bearer {token}"},
        )
        
        assert response.status_code in [422, 400]

    def test_reject_review_reason_too_short(self, client, admin_user, pending_review):
        """Test rejecting review with reason that's too short."""
        token = get_admin_token(client, admin_user)
        
        response = client.put(
            f"/admin/reviews/{pending_review.id}/reject",
            json={"moderation_reason": "Bad"},
            headers={"Authorization": f"Bearer {token}"},
        )
        
        assert response.status_code == 422

    def test_reject_nonexistent_review(self, client, admin_user):
        """Test rejecting a nonexistent review."""
        token = get_admin_token(client, admin_user)
        fake_id = uuid4()
        
        response = client.put(
            f"/admin/reviews/{fake_id}/reject",
            json={"moderation_reason": "Inappropriate content"},
            headers={"Authorization": f"Bearer {token}"},
        )
        
        assert response.status_code == 404
        assert "Review not found" in response.json()["detail"]

    def test_reject_already_rejected_review(
        self, client, admin_user, db_session, sgi
    ):
        """Test rejecting an already rejected review."""
        token = get_admin_token(client, admin_user)
        
        rejected_review = Review(
            id=uuid4(),
            sgi_id=sgi.id,
            rating=2,
            comment="Bad review",
            reviewer_name="Bad User",
            reviewer_email="bad@example.com",
            status=ReviewStatus.REJECTED,
            moderation_reason="Already rejected",
            moderated_by=admin_user.id,
            moderated_at=datetime.utcnow(),
        )
        db_session.add(rejected_review)
        db_session.commit()
        
        response = client.put(
            f"/admin/reviews/{rejected_review.id}/reject",
            json={"moderation_reason": "Another reason"},
            headers={"Authorization": f"Bearer {token}"},
        )
        
        assert response.status_code == 400
        assert "not pending" in response.json()["detail"]

    def test_reject_with_long_reason(self, client, admin_user, pending_review):
        """Test rejecting review with a long detailed reason."""
        token = get_admin_token(client, admin_user)
        long_reason = "This review contains inappropriate language and violates our community guidelines"
        
        response = client.put(
            f"/admin/reviews/{pending_review.id}/reject",
            json={"moderation_reason": long_reason},
            headers={"Authorization": f"Bearer {token}"},
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == ReviewStatus.REJECTED
        assert data["moderation_reason"] == long_reason


class TestModerationWorkflow:
    """Test complete moderation workflows."""

    def test_full_approval_workflow(
        self, client, admin_user, db_session, sgi, regular_user
    ):
        """Test full approval workflow from creation to approval."""
        # Create review
        review = Review(
            id=uuid4(),
            sgi_id=sgi.id,
            user_id=regular_user.id,
            rating=5,
            comment="Great service",
            reviewer_name="Alice",
            reviewer_email="alice@example.com",
            status=ReviewStatus.PENDING,
        )
        db_session.add(review)
        db_session.commit()
        
        token = get_admin_token(client, admin_user)
        
        # Get pending reviews
        response = client.get(
            "/admin/reviews/pending",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1
        
        # Approve the review
        response = client.put(
            f"/admin/reviews/{review.id}/approve",
            json={"moderation_reason": "Quality content"},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        assert response.json()["status"] == ReviewStatus.APPROVED
        
        # Verify it's no longer in pending list
        response = client.get(
            "/admin/reviews/pending",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert not any(r["id"] == str(review.id) for r in data)

    def test_full_rejection_workflow(
        self, client, admin_user, db_session, sgi, regular_user
    ):
        """Test full rejection workflow from creation to rejection."""
        # Create review
        review = Review(
            id=uuid4(),
            sgi_id=sgi.id,
            user_id=regular_user.id,
            rating=1,
            comment="Spam content",
            reviewer_name="Spammer",
            reviewer_email="spam@example.com",
            status=ReviewStatus.PENDING,
        )
        db_session.add(review)
        db_session.commit()
        
        token = get_admin_token(client, admin_user)
        
        # Reject the review
        response = client.put(
            f"/admin/reviews/{review.id}/reject",
            json={"moderation_reason": "Spam and abusive content"},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        assert response.json()["status"] == ReviewStatus.REJECTED
        
        # Verify it's no longer in pending list
        response = client.get(
            "/admin/reviews/pending",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert not any(r["id"] == str(review.id) for r in data)
