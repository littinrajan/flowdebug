"""
Tests for trace filtering.
"""

from __future__ import annotations

from pathlib import Path
from types import CodeType, FrameType
from unittest.mock import Mock

from flowdebug.tracer import Tracer, TracerConfig


def _frame(
    *,
    module: str = "example",
    file: str = "/project/main.py",
    function: str = "main",
) -> FrameType:
    """
    Create a mock frame for testing.
    """
    code = Mock(spec=CodeType)
    code.co_filename = file
    code.co_name = function

    frame = Mock(spec=FrameType)
    frame.f_globals = {"__name__": module}
    frame.f_code = code

    return frame


def test_frame_is_traced_when_no_filters_are_configured() -> None:
    """
    Frames are traced when no filters are configured.
    """
    tracer = Tracer()

    assert tracer._should_trace(_frame())


def test_module_filter_is_applied() -> None:
    """
    Module filtering is applied.
    """
    tracer = Tracer(
        config=TracerConfig(
            include_modules=("example",),
        )
    )

    assert tracer._should_trace(
        _frame(module="example.api")
    )

    assert not tracer._should_trace(
        _frame(module="pytest")
    )


def test_file_filter_is_applied() -> None:
    """
    File filtering is applied.
    """
    tracer = Tracer(
        config=TracerConfig(
            include_files=(Path("/project/src"),),
        )
    )

    assert tracer._should_trace(
        _frame(file="/project/src/main.py")
    )

    assert not tracer._should_trace(
        _frame(file="/project/tests/test_main.py")
    )


def test_function_filter_is_applied() -> None:
    """
    Function filtering is applied.
    """
    tracer = Tracer(
        config=TracerConfig(
            include_functions=("process",),
        )
    )

    assert tracer._should_trace(
        _frame(function="process_data")
    )

    assert not tracer._should_trace(
        _frame(function="helper")
    )


def test_all_filters_must_match() -> None:
    """
    All configured filters must match.
    """
    tracer = Tracer(
        config=TracerConfig(
            include_modules=("example",),
            include_files=(Path("/project/src"),),
            include_functions=("process",),
        )
    )

    assert tracer._should_trace(
        _frame(
            module="example.api",
            file="/project/src/main.py",
            function="process_data",
        )
    )

    assert not tracer._should_trace(
        _frame(
            module="pytest",
            file="/project/src/main.py",
            function="process_data",
        )
    )

    assert not tracer._should_trace(
        _frame(
            module="example.api",
            file="/project/tests/test_main.py",
            function="process_data",
        )
    )

    assert not tracer._should_trace(
        _frame(
            module="example.api",
            file="/project/src/main.py",
            function="helper",
        )
    )
