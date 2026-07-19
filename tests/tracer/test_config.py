"""
Tests for tracer configuration.
"""

from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest

from flowdebug.tracer import TracerConfig, trace


def test_default_configuration() -> None:
    """
    Default tracer configuration is empty.
    """
    config = TracerConfig()

    assert config.include_modules == ()
    assert config.exclude_modules == ()
    assert config.include_files == ()
    assert config.exclude_files == ()
    assert config.include_functions == ()
    assert config.exclude_functions == ()


def test_custom_configuration() -> None:
    """
    Custom tracer configuration is preserved.
    """
    config = TracerConfig(
        include_modules=("example",),
        exclude_functions=("helper",),
    )

    assert config.include_modules == ("example",)
    assert config.exclude_functions == ("helper",)


def test_configuration_is_immutable() -> None:
    """
    Tracer configuration is immutable.
    """
    config = TracerConfig()

    with pytest.raises(FrozenInstanceError):
        config.include_modules = ("new",)  # type: ignore[misc]


def test_trace_accepts_configuration() -> None:
    """
    Trace uses the supplied configuration.
    """
    config = TracerConfig(
        include_modules=("sample",),
    )

    with trace(config=config) as tracer:
        assert tracer.config is config


def test_trace_uses_default_configuration() -> None:
    """
    Trace creates a default configuration when none is provided.
    """
    with trace() as tracer:
        assert tracer.config is not None
        assert tracer.config == TracerConfig()
