import click

from . import commands

@click.group()
def cli():
    pass

cli.add_command(commands.translate)
cli.add_command(commands.transcribe)
