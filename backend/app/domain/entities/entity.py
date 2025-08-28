"""Base entity with domain events support."""

from abc import ABC
from dataclasses import dataclass, field
from typing import List

from .events.domain_event import DomainEvent


@dataclass
class Entity(ABC):
    """Base class for domain entities with domain events support."""
    _domain_events: List[DomainEvent] = field(default_factory=list, init=False)

    def add_domain_event(self, event: DomainEvent) -> None:
        """Add a domain event to the entity."""
        self._domain_events.append(event)

    def clear_domain_events(self) -> List[DomainEvent]:
        """Clear and return all domain events."""
        events = self._domain_events.copy()
        self._domain_events.clear()
        return events

    @property
    def domain_events(self) -> List[DomainEvent]:
        """Get all domain events."""
        return self._domain_events.copy()
