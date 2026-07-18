from __future__ import annotations

from pathlib import Path
import pytest

from flowdebug.core import (
    Event,
    EventType,
    ExecutionContext,
    SourceLocation,
)
from flowdebug.recorder import MemoryRecorder


def create_event(name: str) -> Event:
    return Event(
        event_type=EventType.CALL,
        name=name,
        source=SourceLocation(
            file=Path("example.py"),
            function=name,
            line=1,
        ),
        context=ExecutionContext(
            process_id=1,
            thread_id=1,
            thread_name="MainThread",
        ),
    )


def test_memory_recorder_starts_empty() -> None:
    recorder = MemoryRecorder()

    assert len(recorder.events()) == 0


def test_memory_recorder_records_event() -> None:
    recorder = MemoryRecorder()
    event = create_event("demo")

    recorder.record(event)

    assert recorder.events() == (event,)


def test_memory_recorder_preserves_order() -> None:
    recorder = MemoryRecorder()

    first = create_event("first")
    second = create_event("second")

    recorder.record(first)
    recorder.record(second)

    assert recorder.events() == (first, second)


def test_memory_recorder_clear() -> None:
    recorder = MemoryRecorder()

    recorder.record(create_event("demo"))
    recorder.clear()

    assert recorder.events() == ()


def test_memory_recorder_len() -> None:
    recorder = MemoryRecorder()

    recorder.record(create_event("demo"))

    assert len(recorder) == 1


def test_memory_recorder_bool() -> None:
    recorder = MemoryRecorder()

    assert not recorder

    recorder.record(create_event("demo"))

    assert recorder


def test_memory_recorder_iteration() -> None:
    recorder = MemoryRecorder()

    first = create_event("first")
    second = create_event("second")

    recorder.record(first)
    recorder.record(second)

    assert list(recorder) == [first, second]


def test_memory_recorder_events_are_immutable() -> None:
    recorder = MemoryRecorder()

    recorder.record(create_event("demo"))

    events = recorder.events()

    with pytest.raises(AttributeError):
        events.append(create_event("another"))  # type: ignore[attr-defined]
