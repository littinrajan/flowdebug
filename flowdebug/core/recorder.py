"""
Recorder interfaces.
"""

from __future__ import annotations

from typing import Protocol

from .events import Event


class Recorder(Protocol):
    """
    Common interface implemented by every recorder.
    """

    def record(self, event: Event) -> None:
        """
        Store a single execution event.
        """
        ...

    def clear(self) -> None:
        """
        Remove all recorded events.
        """
        ...

    def events(self) -> list[Event]:
        """
        Return recorded events.
        """
        ...
