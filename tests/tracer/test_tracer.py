"""
Tests for the FlowDebug tracer.
"""

from __future__ import annotations

from pathlib import Path

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


def test_records_exception_event() -> None:
    """
    Function exception events are recorded.
    """

    def sample() -> None:
        raise ValueError("boom")

    with trace() as tracer:
        try:
            sample()
        except ValueError:
            pass

    events = [
        event
        for event in tracer.recorder.events()
        if event.event_type is EventType.EXCEPTION
        and event.name == "sample"
    ]

    assert len(events) == 1

    event = events[0]

    assert event.metadata["exception_type"] == "ValueError"
    assert event.metadata["exception_message"] == "boom"


def test_records_call_exception_and_return_events() -> None:
    """
    Call, exception and return events are recorded.
    """

    def sample() -> None:
        raise RuntimeError("failure")

    with trace() as tracer:
        try:
            sample()
        except RuntimeError:
            pass

    event_types = [
        event.event_type
        for event in tracer.recorder.events()
        if event.name == "sample"
    ]

    assert EventType.CALL in event_types
    assert EventType.EXCEPTION in event_types
    assert EventType.RETURN in event_types


def test_records_line_event() -> None:
    """
    Line events are recorded.
    """

    def sample() -> int:
        x = 1
        y = 2
        return x + y

    with trace() as tracer:
        sample()

    assert any(
        event.event_type is EventType.LINE
        and event.name == "sample"
        for event in tracer.recorder.events()
    )


def test_records_multiple_line_events() -> None:
    """
    Multiple executed lines produce multiple line events.
    """

    def sample() -> int:
        a = 1
        b = 2
        c = a + b
        return c

    with trace() as tracer:
        sample()

    line_events = [
        event
        for event in tracer.recorder.events()
        if event.event_type is EventType.LINE
        and event.name == "sample"
    ]

    assert len(line_events) >= 3


def test_line_event_records_function_name() -> None:
    """
    Line events record the correct function.
    """

    def sample() -> int:
        value = 1
        return value

    with trace() as tracer:
        sample()

    line_event = next(
        event
        for event in tracer.recorder.events()
        if event.event_type is EventType.LINE
        and event.name == "sample"
    )

    assert line_event.source is not None
    assert line_event.source.function == "sample"


def test_line_event_records_file() -> None:
    """
    Line events record the correct source file.
    """

    def sample() -> int:
        value = 1
        return value

    with trace() as tracer:
        sample()

    line_event = next(
        event
        for event in tracer.recorder.events()
        if event.event_type is EventType.LINE
        and event.name == "sample"
    )

    assert line_event.source is not None
    assert line_event.source.file == Path(__file__)


def test_line_event_records_line_number() -> None:
    """
    Line events record a valid source line number.
    """

    def sample() -> int:
        value = 1
        return value

    with trace() as tracer:
        sample()

    line_event = next(
        event
        for event in tracer.recorder.events()
        if event.event_type is EventType.LINE
        and event.name == "sample"
    )

    assert line_event.source is not None
    assert line_event.source.line >= sample.__code__.co_firstlineno


def test_line_events_are_recorded_between_call_and_return() -> None:
    """
    Line events are recorded between call and return events.
    """

    def sample() -> int:
        value = 1
        return value

    with trace() as tracer:
        sample()

    event_types = [
        event.event_type
        for event in tracer.recorder.events()
        if event.name == "sample"
    ]

    assert event_types[0] is EventType.CALL
    assert event_types[-1] is EventType.RETURN
    assert EventType.LINE in event_types[1:-1]
