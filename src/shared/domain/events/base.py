# src/shared/domain/events/base.py
"""Base domain event class."""

from abc import ABC
from datetime import datetime
from typing import Any, Dict
from uuid import UUID, uuid4


class DomainEvent(ABC):
    """Base class for domain events."""
    
    def __init__(self, aggregate_id: UUID, **kwargs: Any):
        self.event_id = uuid4()
        self.aggregate_id = aggregate_id
        self.occurred_at = datetime.utcnow()
        self.data = kwargs
    
    @property
    def event_type(self) -> str:
        """Get event type name."""
        return self.__class__.__name__
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert event to dictionary."""
        return {
            "event_id": str(self.event_id),
            "event_type": self.event_type,
            "aggregate_id": str(self.aggregate_id),
            "occurred_at": self.occurred_at.isoformat(),
            "data": self.data
        }
    
    def __repr__(self) -> str:
        """String representation."""
        return f"{self.event_type}(aggregate_id={self.aggregate_id}, occurred_at={self.occurred_at})"
