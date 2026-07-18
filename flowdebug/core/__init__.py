"""
Core execution models used throughout FlowDebug.

This package contains the foundational types shared by the tracer,
recorder, storage layer, reporters, and plugins.
"""

from .enums import EventType

__all__ = (
    "EventType",
)
