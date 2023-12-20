import os
import click

from typing import Tuple
from bragir.client import initiate_client

from bragir.constants import BLACKLISTED_FILES
from bragir.file import (
    calculate_file_size,
    chunk_content,
    chunk_content_into_srt_parts,
    create_file,
    process_file,
    process_files,
    remove_files,
)
from bragir.languages import Languages, parse_languages
from bragir.messages import PROMPT_HELP
from bragir.path_components import File, SRTPart
from bragir.time import update_timestamps
from bragir.transcriber import transcribe_audio_files
from bragir.translator import translate_srt

@click.command()
@click.option(
    "--file_path", "-f", required=True, type=click.Path(exists=True, file_okay=True)
)
@click.option("--output_path", "-o", type=click.Path(file_okay=True))
@click.option(
    "--api_key",
    "-k",
    required=True,
    envvar="OPENAI_API_KEY",
    help=PROMPT_HELP["api_key"],
)
def transcribe(file_path: str, output_path: str, api_key: str) -> None:
    transcriber = initiate_client(api_key=api_key)

    file_size_mbytes = calculate_file_size(file_path)

    audio_paths: list[str] = [file_path]
    if file_size_mbytes >= 25:
        click.echo(f"Chunking {file_path} into smaller audio files.")
        audio_paths = process_file(file_path)
    
    click.echo(f"Transcribing {file_path}")
    transcripts: list[str] = transcribe_audio_files(transcriber, audio_paths)

    click.echo("Constructing SRT parts")
    videos_srts: list[Tuple[int, list[SRTPart]]] = [
        (order, chunk_content_into_srt_parts(transcript))
        for order, transcript in enumerate(transcripts)
    ]

    click.echo("Updating timestamps")
    sorted_videos = sorted(videos_srts)

    srt_parts: list[SRTPart] = update_timestamps(sorted_videos)

    click.echo("Creating SRT file content")
    contents = "".join([srt_part.srt_format for srt_part in srt_parts])

    if output_path:
        target_path = os.path.expanduser(output_path)
    else:
        root, _ = os.path.splitext(file_path)
        target_path = root + ".srt"

    with open(target_path, "w", encoding="utf-8") as fileIO:
        fileIO.write(contents)
        click.echo(f"Created {target_path} for video {file_path}")

    remove_files(audio_paths)


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
    translator = initiate_client(api_key=api_key)

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
        click.echo(f"Translating {target_file.name} to {target_file.language.value}")
        translated_content = translate_srt(
            translator, target_file, target_file.language.value
        )

        click.echo(f"Translated {target_file.name} to {target_file.language}")

        create_file(target_file, translated_content)
        click.echo(f"Created file {target_file.target_path}")
