"""
Configuration for FlowDebug tracing.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class TracerConfig:
    """
    Configuration options for a tracer.
    """

    include_modules: tuple[str, ...] = ()
    exclude_modules: tuple[str, ...] = ()

    include_files: tuple[str, ...] = ()
    exclude_files: tuple[str, ...] = ()

    include_functions: tuple[str, ...] = ()
    exclude_functions: tuple[str, ...] = ()
