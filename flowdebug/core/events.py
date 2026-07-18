"""
Execution event models.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import UUID, uuid4

from .enums import EventType
from .types import Metadata


@dataclass(slots=True, frozen=True)
class Event:
    """
    Immutable execution event.

    This is the fundamental data structure shared across
    the tracer, recorder, storage, and reporting layers.
    """

    event_type: EventType
    name: str

    timestamp: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    event_id: UUID = field(
        default_factory=uuid4
    )

    metadata: Metadata = field(
        default_factory=dict
    )
