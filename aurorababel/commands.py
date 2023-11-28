import os
import click

from typing import Any
from openai import OpenAI

from aurorababel.constants import BLACKLISTED_FILES
from aurorababel.file import chunk_content, create_translation_file
from aurorababel.languages import Languages, parse_languages, to_output
from aurorababel.messages import PROMPT_HELP
from aurorababel.path_components import File
from aurorababel.timer import timing_decorator
from aurorababel.translator import translate_content


def split_list_at_breakpoints(original_list: list[Any], breakpoints: list[int]):
    result: list[Any] = []
    start_index = 0

    for breakpoint in breakpoints:
        result.append(original_list[start_index:breakpoint])
        start_index = breakpoint

    # Append the remaining elements after the last breakpoint
    result.append(original_list[start_index:])

    return result


@timing_decorator
def translate_srt(translator: OpenAI, file: File, language: str) -> str:
    translated_text = ""

    if len(file.breakpoints) == 0:
        translated_text += translate_content(translator, file.contents, language)
        click.echo(f"Translated the whole file {file.source_path}")

    if len(file.breakpoints) > 0:
        chunks = split_list_at_breakpoints(file.SRTParts, breakpoints=file.breakpoints)
        for i, chunk in enumerate(chunks):
            total = ""
            for part in chunk:
                if i == 0:
                    total += part.srt_format
                else:
                    total += "\n \n" + part.srt_format

            translated_text += translate_content(translator, total, language)

            click.echo(f"Chunk {i + 1} translated")

    return translated_text


def process_files(file_paths: list[str], languages: list[Languages]) -> list[File]:
    processed_files: list[File] = []
    res: list[File] = []
    for file_path in file_paths:
        (content, breakpoints) = chunk_content(file_path)
        for language in languages:
            base_path, file_name = os.path.split(file_path)
            updated_file_name = f"{language.value.lower()[:3]}_{file_name}"
            new_file_path = os.path.join(base_path, updated_file_name)
            file = File(
                name=file_path,
                language=language,
                SRTParts=content,
                breakpoints=breakpoints,
                target_path=new_file_path,
                source_path=file_path,
            )

            processed_files.append(file)

    return res


@click.command()
@click.option(
    "--file",
    "-f",
    type=click.Path(dir_okay=True, exists=True),
    prompt="Enter path to file",
    help=PROMPT_HELP["file"],
)
@click.option(
    "--api_key",
    "-k",
    required=True, 
    envvar="OPENAI_API_KEY",
    help=PROMPT_HELP["api_key"],
)
@click.option(
    "--directory",
    "-d",
    type=click.Path(dir_okay=True, exists=True),
    help=PROMPT_HELP["directory"],
)
@click.option(
    "--language",
    "-l",
    required=True, 
    type=click.Choice([language.value for language in Languages], case_sensitive=False),
    multiple=True,
    help=PROMPT_HELP["language"],
)
def translate(file: str, api_key: str, language: str, directory: str) -> None:
    if not api_key:
        click.echo("Can not initiate openai translator, please give an api key")
        exit()

    translator = ""
    if api_key:
        translator = OpenAI(
            api_key=api_key,
        )
    else:
        click.echo("Couldn't initate openai translator")
        exit()

    if not directory and not file:
        click.echo("Please provide a file or directory")
        exit()

    translate_to_languages: list[Languages] = parse_languages(language)

    click.echo(
        f"Translating to following language/languages: {' '.join([language.value for language in translate_to_languages])}"
    )

    files: list[File] = []
    if file:
        click.echo(f"Translating file {file}")
        for target_language in translate_to_languages:
            base_path, file_name = os.path.split(file)
            updated_file_name = f"{target_language.value.lower()[:3]}_{file_name}"
            new_file_path = os.path.join(base_path, updated_file_name)

            (contents, breakpoints) = chunk_content(file)

            files.append(
                File(
                    name=file,
                    language=target_language,
                    SRTParts=contents,
                    breakpoints=breakpoints,
                    target_path=new_file_path,
                    source_path=file,
                )
            )

    if directory:
        directory_file_paths: list[str] = []
        # Walk through the directory and its subdirectories
        for root, _dirs, nested_files in os.walk(directory):
            for nested_file in nested_files:
                if nested_file not in BLACKLISTED_FILES:
                    # Create the full path to the file
                    directory_file_paths.append(os.path.join(root, nested_file))

        num_of_file_paths = len(directory_file_paths)

        if num_of_file_paths == 1:
            click.echo(f"Processing {num_of_file_paths} file in directory {directory}")
        else:
            click.echo(f"Processing {num_of_file_paths} files in directory {directory}")

        files = process_files(directory_file_paths, translate_to_languages)

    num_of_file_paths = len(files)

    if num_of_file_paths == 1:
        click.echo(f"Processing {num_of_file_paths} file")
    else:
        click.echo(f"Processing {num_of_file_paths} files")

    for target_file in files:
        click.echo(f"Translating {target_file.name} to {target_file.language}")
        translated_content = translate_srt(
            translator, target_file, target_file.language.value
        )

        click.echo(f"Translated {target_file.name} to {target_file.language}")

        click.echo(f"Creating target_file {target_file.target_path}")
        create_translation_file(target_file, translated_content)
        click.echo(f"Created target_file {target_file.target_path}")
