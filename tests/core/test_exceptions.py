from flowdebug.core import (
    FlowDebugError,
    RecorderError,
    TracerError,
)


def test_recorder_error_inherits_base() -> None:
    assert issubclass(RecorderError, FlowDebugError)


def test_tracer_error_inherits_base() -> None:
    assert issubclass(TracerError, FlowDebugError)


def test_raise_base_exception() -> None:
    try:
        raise RecorderError("failure")
    except FlowDebugError as exc:
        assert str(exc) == "failure"
