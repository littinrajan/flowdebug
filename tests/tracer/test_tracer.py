"""
Tests for the FlowDebug tracer.
"""

from __future__ import annotations

from flowdebug.core import EventType
from flowdebug.tracer import trace


def test_trace_returns_tracer() -> None:
    """
    The trace context manager returns a Tracer instance.
    """
    with trace() as tracer:
        assert tracer is not None


def test_records_call_event() -> None:
    """
    Function call events are recorded.
    """

    def sample() -> None:
        pass

    with trace() as tracer:
        sample()

    events = [
        event
        for event in tracer.recorder.events()
        if event.event_type is EventType.CALL
        and event.name == "sample"
    ]

    assert len(events) == 1


def test_records_return_event() -> None:
    """
    Function return events are recorded.
    """

    def sample() -> int:
        return 42

    with trace() as tracer:
        sample()

    events = [
        event
        for event in tracer.recorder.events()
        if event.event_type is EventType.RETURN
        and event.name == "sample"
    ]

    assert len(events) == 1
    assert events[0].metadata["return_value"] == 42


def test_records_call_and_return_events() -> None:
    """
    Both call and return events are recorded.
    """

    def sample() -> int:
        return 10

    with trace() as tracer:
        sample()

    event_types = [
        event.event_type
        for event in tracer.recorder.events()
        if event.name == "sample"
    ]

    assert EventType.CALL in event_types
    assert EventType.RETURN in event_types
