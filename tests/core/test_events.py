from pathlib import Path

import pytest

from flowdebug.core import (
    Event,
    EventType,
    ExecutionContext,
    SourceLocation,
)


def test_create_event() -> None:
    location = SourceLocation(
        file=Path("example.py"),
        function="calculate",
        line=42,
    )

    context = ExecutionContext(
        process_id=1234,
        thread_id=1,
        thread_name="MainThread",
    )

    event = Event(
        event_type=EventType.CALL,
        name="calculate",
        source=location,
        context=context,
    )

    assert event.name == "calculate"
    assert event.event_type is EventType.CALL
    assert event.source == location
    assert event.context == context
    assert event.metadata == {}


def test_event_is_immutable() -> None:
    event = Event(
        event_type=EventType.CALL,
        name="demo",
    )

    with pytest.raises(AttributeError):
        event.name = "changed"  # type: ignore[misc]  # Testing immutability.
