"""
Tracing context manager.
"""

from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager

from .engine import Tracer


@contextmanager
def trace() -> Iterator[Tracer]:
    """
    Create a tracing context.
    """
    tracer = Tracer()

    tracer.start()

    try:
        yield tracer
    finally:
        tracer.stop()
