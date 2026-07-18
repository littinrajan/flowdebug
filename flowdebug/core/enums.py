"""
Enumeration definitions for FlowDebug.
"""

from enum import Enum


class EventType(str, Enum):
    """Supported execution event types."""

    CALL = "call"
    RETURN = "return"
    EXCEPTION = "exception"

    LINE = "line"

    VARIABLE_CREATED = "variable_created"
    VARIABLE_UPDATED = "variable_updated"
    VARIABLE_DELETED = "variable_deleted"

    IMPORT = "import"

    THREAD_START = "thread_start"
    THREAD_END = "thread_end"

    TASK_START = "task_start"
    TASK_END = "task_end"

    FILE_OPEN = "file_open"
    FILE_CLOSE = "file_close"

    HTTP_REQUEST = "http_request"
    HTTP_RESPONSE = "http_response"

    SQL_QUERY = "sql_query"

    LOG = "log"

