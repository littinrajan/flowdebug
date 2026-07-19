"""
Enumeration definitions for FlowDebug.
"""

from enum import Enum


class EventType(str, Enum):
    """Supported execution event types."""

    # Execution
    CALL = "call"
    RETURN = "return"
    EXCEPTION = "exception"
    LINE = "line"

    # Variables
    VARIABLE_CREATED = "variable_created"
    VARIABLE_UPDATED = "variable_updated"
    VARIABLE_DELETED = "variable_deleted"

    # Imports
    IMPORT = "import"

    # Threads
    THREAD_START = "thread_start"
    THREAD_END = "thread_end"

    # Async Tasks
    TASK_START = "task_start"
    TASK_END = "task_end"

    # Files
    FILE_OPEN = "file_open"
    FILE_CLOSE = "file_close"

    # HTTP
    HTTP_REQUEST = "http_request"
    HTTP_RESPONSE = "http_response"

    # Database
    SQL_QUERY = "sql_query"

    # Logging
    LOG = "log"
