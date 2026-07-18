from typing import Annotated

import typer
from rich import print

from flowdebug import __version__


def version(
    verbose: Annotated[
        bool,
        typer.Option(
            "--verbose",
            "-v",
            help="Display additional version information.",
        ),
    ] = False,
) -> None:
    """Display the installed FlowDebug version."""

    print(f"[bold cyan]FlowDebug[/bold cyan] v{__version__}")

    if verbose:
        print("Python execution tracing toolkit.")
