"""
Recorder interfaces.
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Protocol, runtime_checkable

from .events import Event


@runtime_checkable
class Recorder(Protocol):
    """
    Common interface implemented by every FlowDebug recorder.
    """

    def record(self, event: Event) -> None:
        """
        Record a single execution event.
        """
        ...

    def clear(self) -> None:
        """
        Remove all recorded events.
        """
        ...

    def events(self) -> Sequence[Event]:
        """
        Return an immutable view of the recorded events.
        """
        ...
