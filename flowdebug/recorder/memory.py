"""
In-memory recorder implementation.
"""

from __future__ import annotations

from collections.abc import Iterator, Sequence

from flowdebug.core import Event, Recorder


class MemoryRecorder(Recorder):
    """
    Recorder implementation that stores events in memory.
    """

    def __init__(self) -> None:
        self._events: list[Event] = []

    def record(self, event: Event) -> None:
        """
        Record an execution event.
        """
        self._events.append(event)

    def clear(self) -> None:
        """
        Remove all recorded events.
        """
        self._events.clear()

    def events(self) -> Sequence[Event]:
        """
        Return a read-only view of recorded events.
        """
        return tuple(self._events)

    def __len__(self) -> int:
        """
        Return the number of recorded events.
        """
        return len(self._events)

    def __iter__(self) -> Iterator[Event]:
        """
        Iterate over recorded events.
        """
        return iter(self._events)

    def __bool__(self) -> bool:
        """
        Return True when events have been recorded.
        """
        return bool(self._events)
