"""
Tracing engine.
"""

from __future__ import annotations

import sys
from types import FrameType
from typing import Any

from flowdebug.core import Recorder
from flowdebug.recorder import MemoryRecorder


class Tracer:
    """
    Coordinates execution tracing.
    """

    def __init__(self, recorder: Recorder | None = None) -> None:
        self.recorder: Recorder = recorder or MemoryRecorder()

    def start(self) -> None:
        """
        Start execution tracing.
        """
        sys.settrace(self._trace)

    def stop(self) -> None:
        """
        Stop execution tracing.
        """
        sys.settrace(None)

    def _trace(
        self,
        frame: FrameType,
        event: str,
        arg: Any,
    ) -> Any:
        """
        Internal trace callback.

        Event recording is implemented in later steps.
        """
        _ = frame, event, arg

        return self._trace
