"""
Configuration for FlowDebug tracing.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True, slots=True)
class TracerConfig:
    """
    Configuration for execution tracing.
    """

    include_modules: tuple[str, ...] = field(default_factory=tuple)
    exclude_modules: tuple[str, ...] = field(default_factory=tuple)

    include_files: tuple[Path, ...] = field(default_factory=tuple)
    exclude_files: tuple[Path, ...] = field(default_factory=tuple)

    include_functions: tuple[str, ...] = field(default_factory=tuple)
    exclude_functions: tuple[str, ...] = field(default_factory=tuple)
