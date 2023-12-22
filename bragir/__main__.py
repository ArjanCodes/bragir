import click

from . import commands

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    """
    Bragir is an tool that can generate SRT files from videos and translate SRT files.

    In order to use Bragir, an OpenAI api_key needs to be passed as an option. Or alternativly,
    as an enviroment variable in the current session
    """
    pass

cli.add_command(commands.translate)
cli.add_command(commands.transcribe)
