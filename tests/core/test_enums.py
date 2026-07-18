from flowdebug.core import EventType


def test_event_type_values() -> None:
    assert EventType.CALL.value == "call"
    assert EventType.RETURN.value == "return"
    assert EventType.EXCEPTION.value == "exception"


def test_event_type_is_enum() -> None:
    assert isinstance(EventType.CALL, EventType)
