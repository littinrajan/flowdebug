"""
Tracing engine.
"""

from __future__ import annotations

import sys
from pathlib import Path
from types import FrameType, TracebackType
from typing import Any

from flowdebug.core import (
    Event,
    EventType,
    Recorder,
    SourceLocation,
)
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
        if event == "call":
            self._record_call(frame)
        elif event == "return":
            self._record_return(frame, arg)
        elif event == "exception":
            self._record_exception(frame, arg)

        return self._trace

    def _record_call(self, frame: FrameType) -> None:
        """
        Record a function call event.
        """
        self.recorder.record(
            Event(
                event_type=EventType.CALL,
                name=frame.f_code.co_name,
                source=SourceLocation(
                    file=Path(frame.f_code.co_filename),
                    line=frame.f_lineno,
                    function=frame.f_code.co_name,
                ),
            )
        )

    def _record_return(
        self,
        frame: FrameType,
        value: Any,
    ) -> None:
        """
        Record a function return event.
        """
        self.recorder.record(
            Event(
                event_type=EventType.RETURN,
                name=frame.f_code.co_name,
                source=SourceLocation(
                    file=Path(frame.f_code.co_filename),
                    line=frame.f_lineno,
                    function=frame.f_code.co_name,
                ),
                metadata={
                    "return_value": value,
                },
            )
        )

    def _record_exception(
        self,
        frame: FrameType,
        arg: tuple[
            type[BaseException],
            BaseException,
            TracebackType | None,
        ],
    ) -> None:
        """
        Record a function exception event.
        """
        exception_type, exception, _ = arg

        self.recorder.record(
            Event(
                event_type=EventType.EXCEPTION,
                name=frame.f_code.co_name,
                source=SourceLocation(
                    file=Path(frame.f_code.co_filename),
                    line=frame.f_lineno,
                    function=frame.f_code.co_name,
                ),
                metadata={
                    "exception_type": exception_type.__name__,
                    "exception_message": str(exception),
                },
            )
        )
