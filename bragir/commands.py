import os
import click

from typing import Tuple
from bragir.logger import logger
from bragir.client import initiate_client

from bragir.constants import BLACKLISTED_FILES
from bragir.file import (
    chunk_content,
    chunk_content_into_srt_parts,
    get_new_file_path,
    process_files,
)
from bragir.files.file import File
from bragir.files.operations import create_file
from bragir.languages import Languages, parse_languages
from bragir.messages import PROMPT_HELP
from bragir.path import get_files_in_directory
from bragir.srt.srt_part import SRTPart
from bragir.time import update_timestamps
from bragir.transcription import transcribe_file
from bragir.translation import translate_srt


@click.command(options_metavar="<options>")
@click.option(
    "--file_path",
    "-f",
    type=click.Path(exists=True, file_okay=True),
    help=PROMPT_HELP["file_path"],
    metavar="<path>",
)
@click.option(
    "--directory_path",
    "-d",
    type=click.Path(exists=True, file_okay=True),
    help=PROMPT_HELP["directory"],
    metavar="<path>",
)
@click.option(
    "--output_path",
    "-o",
    type=click.Path(file_okay=True),
    help=PROMPT_HELP["output_path"],
)
@click.option(
    "--api_key",
    "-k",
    required=True,
    envvar="OPENAI_API_KEY",
    help=PROMPT_HELP["api_key"],
)
def transcribe(
    file_path: str, directory_path: str, output_path: str, api_key: str
) -> None:
    """
    The transcribe command generates an SRT file based on an .mp4 or .mp3 file.
    If output is not set, then it will take the file_path name and change the extension.
    """
    logger.info("Starting transcription")
    if not directory_path and not file_path:
        logger.info("Please provide a file or directory")
        exit(1)

    transcriber = initiate_client(api_key=api_key)

    file_paths: list[str] = []

    if directory_path:
        directory_file_paths = get_files_in_directory(directory_path)
        file_paths = [*file_paths, *directory_file_paths]

    if file_path:
        file_paths.append(file_path)

    logger.info(f"Starting transcription of {file_path}")

    for path in file_paths:
        transcripts: list[str] = transcribe_file(transcriber, path)

        videos_srts: list[Tuple[int, list[SRTPart]]] = [
            (order, chunk_content_into_srt_parts(transcript))
            for order, transcript in enumerate(transcripts)
        ]

        sorted_videos = sorted(videos_srts)

        srt_parts: list[SRTPart] = update_timestamps(sorted_videos)

        contents = "".join([srt_part.srt_format for srt_part in srt_parts])

        if output_path:
            target_path = os.path.expanduser(output_path)
        else:
            root, _ = os.path.splitext(path)
            target_path = root + ".srt"

        with open(target_path, "w", encoding="utf-8") as fileIO:
            fileIO.write(contents)
            logger.info(f"Created {target_path} for video {path}")
            click.echo(f"Created {target_path} for video {path}")


@click.command(options_metavar="<options>")
@click.option(
    "--file",
    "-f",
    type=click.Path(dir_okay=True, exists=True),
    prompt="Enter path to file",
    help=PROMPT_HELP["file"],
    metavar="<path>",
)
@click.option(
    "--directory",
    "-d",
    type=click.Path(dir_okay=True, exists=True),
    help=PROMPT_HELP["directory"],
    metavar="<directory>",
)
@click.option(
    "--api_key",
    "-k",
    required=True,
    envvar="OPENAI_API_KEY",
    help=PROMPT_HELP["api_key"],
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
    """
    The translate command, translates either a single SRT file or files or directory of SRT files into the wanted language.
    """
    logger.info("Starting transcription")

    translator = initiate_client(api_key=api_key)

    if not directory and not file:
        click.echo("Please provide a file or directory")
        exit()

    translate_to_languages: list[Languages] = parse_languages(language)

    logger.info(
        f"Translating to following language/languages: {' '.join([language.value for language in translate_to_languages])}"
    )

    files: list[File] = []
    if file:
        logger.info(f"Adding file {file} for translation")

        for target_language in translate_to_languages:
            logger.info(
                f"Adding file {file} with {target_language.value} for translation"
            )

            new_file_path = get_new_file_path(file, target_language)

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
                    logger.info(f"Adding file {nested_file} for translation")
                    directory_file_paths.append(os.path.join(root, nested_file))

        num_of_file_paths = len(directory_file_paths)

        if num_of_file_paths == 1:
            logger.info(f"Processing {num_of_file_paths} file in directory {directory}")
        else:
            logger.info(
                f"Processing {num_of_file_paths} files in directory {directory}"
            )

        files = process_files(directory_file_paths, translate_to_languages)

    num_of_file_paths = len(files)

    if num_of_file_paths == 1:
        logger.info(f"Processing {num_of_file_paths} file")
    else:
        logger.info(f"Processing {num_of_file_paths} files")

    for target_file in files:
        translated_content = translate_srt(
            translator, target_file, target_file.language.value
        )
        create_file(target_file, translated_content)

        click.echo(f"Created file {target_file.target_path}")
