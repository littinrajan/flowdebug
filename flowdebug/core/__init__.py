"""
Core execution models used throughout FlowDebug.
"""

from .enums import EventType
from .events import Event

__all__ = (
    "Event",
    "EventType",
)
