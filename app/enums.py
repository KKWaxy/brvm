"""
Enumerations for the application.
"""

from enum import Enum


class ReviewStatus(str, Enum):
    """Review moderation status."""

    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
