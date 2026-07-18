import typer

from flowdebug.cli.commands.doctor import doctor
from flowdebug.cli.commands.init import init
from flowdebug.cli.commands.run import run
from flowdebug.cli.commands.version import version

app = typer.Typer(
    name="flowdebug",
    help="Interactive execution tracing toolkit.",
    no_args_is_help=True,
)

app.command()(version)
app.command()(doctor)
app.command(name="init")(init)
app.command()(run)

if __name__ == "__main__":
    app()
