"""
Tracing context manager.
"""

from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager

from flowdebug.core import Recorder

from .config import TracerConfig
from .engine import Tracer


@contextmanager
def trace(
    *,
    recorder: Recorder | None = None,
    config: TracerConfig | None = None,
) -> Iterator[Tracer]:
    """
    Create a tracing context.
    """
    tracer = Tracer(
        recorder=recorder,
        config=config,
    )

    tracer.start()

    try:
        yield tracer
    finally:
        tracer.stop()
