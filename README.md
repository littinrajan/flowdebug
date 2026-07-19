# FlowDebug

> Interactive execution tracing and visualization toolkit for Python.

FlowDebug helps developers understand how Python applications execute by capturing runtime events such as function calls, executed source lines, function returns, and exceptions.

> 🚧 This project is currently under active development.

## Current Features

- ✅ Function call tracing
- ✅ Source line tracing
- ✅ Function return tracing
- ✅ Exception tracing
- ✅ Configurable module filtering
- ✅ Configurable file filtering
- ✅ Configurable function filtering
- ✅ In-memory event recorder

## Planned Features

- Variable inspection
- Execution timeline
- Interactive HTML reports
- Plugin architecture
- FastAPI integration
- Django integration
- SQLAlchemy integration
- AI-assisted execution analysis

## Installation

```bash
pip install -e .
```

## Quick Example

```python
from flowdebug.tracer import trace


def greet(name: str) -> str:
    message = f"Hello, {name}"
    print(message)
    return message


with trace() as tracer:
    greet("World")

for event in tracer.recorder.events():
    print(event.event_type, event.name)
```

Example output:

```text
CALL greet
LINE greet
LINE greet
RETURN greet
```

## Development

Install development dependencies.

```bash
pip install -e ".[dev]"
```

## License

MIT License
