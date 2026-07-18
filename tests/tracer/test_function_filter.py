"""
Tests for function filtering.
"""

from __future__ import annotations

from flowdebug.tracer import Tracer, TracerConfig


def test_empty_configuration_traces_all_functions() -> None:
    """
    Empty configuration traces every function.
    """
    tracer = Tracer()

    assert tracer._should_trace_function("main")
    assert tracer._should_trace_function("helper")
    assert tracer._should_trace_function("_private")


def test_include_functions_only() -> None:
    """
    Included functions are traced.
    """
    tracer = Tracer(
        config=TracerConfig(
            include_functions=("main",),
        )
    )

    assert tracer._should_trace_function("main")
    assert tracer._should_trace_function("main_loop")

    assert not tracer._should_trace_function("helper")
    assert not tracer._should_trace_function("process")


def test_exclude_functions() -> None:
    """
    Excluded functions are not traced.
    """
    tracer = Tracer(
        config=TracerConfig(
            exclude_functions=("helper",),
        )
    )

    assert tracer._should_trace_function("main")
    assert tracer._should_trace_function("process")

    assert not tracer._should_trace_function("helper")
    assert not tracer._should_trace_function("helper_internal")


def test_include_functions_take_priority_over_exclude_functions() -> None:
    """
    Included functions take priority over excluded functions.
    """
    tracer = Tracer(
        config=TracerConfig(
            include_functions=("main",),
            exclude_functions=("main", "helper"),
        )
    )

    assert tracer._should_trace_function("main")
    assert tracer._should_trace_function("main_loop")

    assert not tracer._should_trace_function("helper")
    assert not tracer._should_trace_function("process")


def test_function_filter_uses_prefix_matching() -> None:
    """
    Function filtering uses prefix matching.
    """
    tracer = Tracer(
        config=TracerConfig(
            include_functions=("process",),
        )
    )

    assert tracer._should_trace_function("process")
    assert tracer._should_trace_function("process_data")
    assert tracer._should_trace_function("process_request")

    assert not tracer._should_trace_function("helper")
