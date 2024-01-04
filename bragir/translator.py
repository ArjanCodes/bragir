import click
from openai import OpenAI
from bragir.list import split_list_at_breakpoints
from bragir.path_components import File

from bragir.timer import timing_decorator


def translate_content(client: OpenAI, text: str, language: str) -> str:
    completion = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[
            {
                "role": "system",
                "content": f"You are a translator machine, you can only translate to the following language {language}. You need to keep the exact same format as the file. only translate the pieces of text. Make sure that all the text is translated and that there are no timestamps missing. Don't add any whitespace on the first line of the file or the last line of the file",
            },
            {"role": "user", "content": text},
        ],
    )

    return completion.choices[0].message.content or ""


@timing_decorator
def translate_srt(translator: OpenAI, file: File, language: str) -> str:
    translated_text = ""

    if len(file.breakpoints) == 0:
        translated_text += translate_content(translator, file.contents, language)
        click.echo(f"Translated the whole file {file.source_path}")

    if len(file.breakpoints) > 0:
        chunks = split_list_at_breakpoints(file.SRTParts, breakpoints=file.breakpoints)

        for i, chunk in enumerate(chunks):
            text = ""
            for part in chunk:
                text += part.srt_format
            text.rstrip("\n")

            translated_text += translate_content(translator, text, language)

            # Add new block onto the text
            translated_text += "\n\n"

            click.echo(f"Chunk {i + 1} translated")

    return translated_text
