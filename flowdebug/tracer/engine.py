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

from .config import TracerConfig


class Tracer:
    """
    Coordinates execution tracing.
    """

    def __init__(
        self,
        recorder: Recorder | None = None,
        config: TracerConfig | None = None,
    ) -> None:
        self.recorder: Recorder = recorder or MemoryRecorder()
        self.config: TracerConfig = config or TracerConfig()
        self._previous_locals: dict[int, dict[str, object]] = {}

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
        Trace execution events.
        """
        if not self._should_trace(frame):
            return self._trace

        if event == "call":
            self._record_call(frame)
        elif event == "line":
            self._record_line(frame)
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

    def _record_line(
        self,
        frame: FrameType,
    ) -> None:
        """
        Record a line execution event.
        """
        self.recorder.record(
            Event(
                event_type=EventType.LINE,
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

    def _should_trace_module(self, module: str) -> bool:
        """
        Determine whether a module should be traced.
        """
        include = self.config.include_modules
        exclude = self.config.exclude_modules

        if include:
            return module.startswith(include)

        if exclude:
            return not module.startswith(exclude)

        return True

    def _should_trace_file(self, file: Path) -> bool:
        """
        Determine whether a file should be traced.
        """
        include = self.config.include_files
        exclude = self.config.exclude_files

        if include:
            return any(
                file == path or file.is_relative_to(path)
                for path in include
            )

        if exclude:
            return not any(
                file == path or file.is_relative_to(path)
                for path in exclude
            )

        return True

    def _should_trace_function(self, function: str) -> bool:
        """
        Determine whether a function should be traced.
        """
        include = self.config.include_functions
        exclude = self.config.exclude_functions

        if include:
            return function.startswith(include)

        if exclude:
            return not function.startswith(exclude)

        return True

    def _should_trace(self, frame: FrameType) -> bool:
        """
        Determine whether a frame should be traced.
        """
        module = str(frame.f_globals.get("__name__", ""))
        file = Path(frame.f_code.co_filename)
        function = frame.f_code.co_name

        return (
            self._should_trace_module(module)
            and self._should_trace_file(file)
            and self._should_trace_function(function)
        )

    def _get_frame_locals(
        self,
        frame: FrameType,
    ) -> dict[str, object]:
        """
        Return a shallow copy of a frame's local variables.
        """
        return dict(frame.f_locals)
