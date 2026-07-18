"""
Tests for file filtering.
"""

from __future__ import annotations

from pathlib import Path

from flowdebug.tracer import Tracer, TracerConfig


def test_empty_configuration_traces_all_files() -> None:
    """
    Empty configuration traces every file.
    """
    tracer = Tracer()

    assert tracer._should_trace_file(Path("/project/main.py"))
    assert tracer._should_trace_file(Path("/project/tests/test_main.py"))


def test_include_files_only() -> None:
    """
    Included files are traced.
    """
    tracer = Tracer(
        config=TracerConfig(
            include_files=(Path("/project/src"),),
        )
    )

    assert tracer._should_trace_file(
        Path("/project/src/main.py")
    )

    assert tracer._should_trace_file(
        Path("/project/src/api/routes.py")
    )

    assert not tracer._should_trace_file(
        Path("/project/tests/test_main.py")
    )


def test_exclude_files() -> None:
    """
    Excluded files are not traced.
    """
    tracer = Tracer(
        config=TracerConfig(
            exclude_files=(Path("/project/tests"),),
        )
    )

    assert tracer._should_trace_file(
        Path("/project/src/main.py")
    )

    assert not tracer._should_trace_file(
        Path("/project/tests/test_main.py")
    )

    assert not tracer._should_trace_file(
        Path("/project/tests/unit/test_api.py")
    )


def test_include_files_take_priority_over_exclude_files() -> None:
    """
    Included files take priority over excluded files.
    """
    tracer = Tracer(
        config=TracerConfig(
            include_files=(Path("/project/src"),),
            exclude_files=(
                Path("/project/src"),
                Path("/project/tests"),
            ),
        )
    )

    assert tracer._should_trace_file(
        Path("/project/src/main.py")
    )

    assert tracer._should_trace_file(
        Path("/project/src/api/routes.py")
    )

    assert not tracer._should_trace_file(
        Path("/project/tests/test_main.py")
    )


def test_include_file_matches_exact_path() -> None:
    """
    Exact file matches are traced.
    """
    tracer = Tracer(
        config=TracerConfig(
            include_files=(
                Path("/project/main.py"),
            ),
        )
    )

    assert tracer._should_trace_file(
        Path("/project/main.py")
    )

    assert not tracer._should_trace_file(
        Path("/project/utils.py")
    )
