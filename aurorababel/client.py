
import click
from openai import OpenAI


def initiate_client(api_key: str) -> OpenAI:
    if not api_key:
        click.echo("Cannot initiate OpenAI client, please provide an API key.")
        exit()

    return OpenAI(api_key=api_key)