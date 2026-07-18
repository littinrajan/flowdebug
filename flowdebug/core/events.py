"""
Execution event models.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from uuid import UUID, uuid4

from .enums import EventType
from .types import Metadata


@dataclass(slots=True, frozen=True)
class SourceLocation:
    """
    Represents a location in a Python source file.
    """

    file: Path
    function: str
    line: int


@dataclass(slots=True, frozen=True)
class ExecutionContext:
    """
    Runtime information captured during execution.
    """

    process_id: int
    thread_id: int
    thread_name: str


@dataclass(slots=True, frozen=True)
class Event:
    """
    Immutable execution event.
    """

    event_type: EventType
    name: str

    timestamp: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    event_id: UUID = field(
        default_factory=uuid4
    )

    source: SourceLocation | None = None

    context: ExecutionContext | None = None

    metadata: Metadata = field(
        default_factory=dict
    )
