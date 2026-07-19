"""
Tests for module filtering.
"""

from __future__ import annotations

from flowdebug.tracer import Tracer, TracerConfig


def test_empty_configuration_traces_all_modules() -> None:
    """
    Empty configuration traces every module.
    """
    tracer = Tracer()

    assert tracer._should_trace_module("example")
    assert tracer._should_trace_module("example.api")
    assert tracer._should_trace_module("pytest")
    assert tracer._should_trace_module("flowdebug")


def test_include_modules_only() -> None:
    """
    Included modules are traced.
    """
    tracer = Tracer(
        config=TracerConfig(
            include_modules=("example",),
        )
    )

    assert tracer._should_trace_module("example")
    assert tracer._should_trace_module("example.api")

    assert not tracer._should_trace_module("pytest")
    assert not tracer._should_trace_module("requests")
    assert not tracer._should_trace_module("flowdebug")


def test_exclude_modules() -> None:
    """
    Excluded modules are not traced.
    """
    tracer = Tracer(
        config=TracerConfig(
            exclude_modules=("pytest",),
        )
    )

    assert tracer._should_trace_module("example")
    assert tracer._should_trace_module("example.api")

    assert not tracer._should_trace_module("pytest")
    assert not tracer._should_trace_module("pytest.assertion")


def test_include_modules_take_priority_over_exclude_modules() -> None:
    """
    Include modules take priority over excluded modules.
    """
    tracer = Tracer(
        config=TracerConfig(
            include_modules=("example",),
            exclude_modules=("example", "pytest"),
        )
    )

    assert tracer._should_trace_module("example")
    assert tracer._should_trace_module("example.api")

    assert not tracer._should_trace_module("pytest")
    assert not tracer._should_trace_module("requests")


def test_include_module_prefix_matching() -> None:
    """
    Module filtering uses prefix matching.
    """
    tracer = Tracer(
        config=TracerConfig(
            include_modules=("flowdebug",),
        )
    )

    assert tracer._should_trace_module("flowdebug")
    assert tracer._should_trace_module("flowdebug.core")
    assert tracer._should_trace_module("flowdebug.tracer")

    assert not tracer._should_trace_module("pytest")
