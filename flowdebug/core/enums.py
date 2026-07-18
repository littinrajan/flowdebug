"""
Enumeration definitions for FlowDebug.
"""

from enum import Enum


class EventType(str, Enum):
    """
    Types of execution events captured by FlowDebug.
    """

    CALL = "call"
    RETURN = "return"
    EXCEPTION = "exception"
