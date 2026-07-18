"""
Core exception hierarchy for FlowDebug.
"""


class FlowDebugError(Exception):
    """
    Base exception for all FlowDebug errors.
    """


class RecorderError(FlowDebugError):
    """
    Raised when an event recorder fails.
    """


class TracerError(FlowDebugError):
    """
    Raised when the execution tracer encounters an error.
    """


class StorageError(FlowDebugError):
    """
    Raised when an event storage backend fails.
    """


class ReporterError(FlowDebugError):
    """
    Raised when report generation fails.
    """


class PluginError(FlowDebugError):
    """
    Raised when a plugin fails during execution.
    """


class ConfigurationError(FlowDebugError):
    """
    Raised when FlowDebug configuration is invalid.
    """
