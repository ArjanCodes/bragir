import os
import click
from bragir.directory import get_files_in_directory
from bragir.client import initiate_client
from bragir.file import (
    chunk_content,
    chunk_content_into_srt_parts,
    get_new_file_path,
    process_files,
)
from bragir.files.file import File
from bragir.files.operations import create_file
from bragir.languages import Languages, parse_languages
from bragir.spinner import spinner
from bragir.tracing.logger import logger
from bragir.messages import PROMPT_HELP
from bragir.path import get_target_path
from bragir.srt.srt_part import SRTPart
from bragir.time import update_timestamps
from bragir.transcription import transcribe_file
from bragir.translation import translate_srt


@click.command(options_metavar="<options>")
@click.argument(
    "path",
    type=click.Path(exists=True, file_okay=True, dir_okay=True),
    metavar="<path>",
)
@click.argument(
    "output",
    type=click.Path(exists=False, file_okay=True, dir_okay=True, writable=True),
    required=False,
)
@click.option(
    "--api_key",
    "-k",
    required=True,
    envvar="OPENAI_API_KEY",
    help=PROMPT_HELP["api_key"],
)
@spinner("transcribe")
def transcribe(path: str, output: str, api_key: str) -> None:
    """
    The transcribe command generates an SRT file based on an .mp4 or .mp3 file.
    If output is not set, then it will take the file_path name and change the extension.
    """
    logger.info("Starting transcription")

    path_is_file = os.path.isfile(path)
    path_is_directory = os.path.isdir(path)

    if not path_is_file and not path_is_directory:
        logger.info("Please provide a file or directory")
        exit(1)

    transcriber = initiate_client(api_key=api_key)

    file_paths: list[str] = []

    if path_is_directory:
        directory_file_paths = get_files_in_directory(path)
        file_paths = [*file_paths, *directory_file_paths]

    if path_is_file:
        file_paths.append(path)

    logger.info(f"Starting transcription of {path}")

    for file_path in file_paths:
        transcripts: list[str] = transcribe_file(transcriber, file_path)

        videos_srts: list[tuple[int, list[SRTPart]]] = [
            (order, chunk_content_into_srt_parts(transcript))
            for order, transcript in enumerate(transcripts)
        ]

        sorted_videos = sorted(videos_srts)

        srt_parts: list[SRTPart] = update_timestamps(sorted_videos)

        contents = "".join([srt_part.srt_format for srt_part in srt_parts])

        target_path = get_target_path(file_path, output)

        with open(target_path, "w", encoding="utf-8") as fileIO:
            fileIO.write(contents)
            logger.info(f"Created {target_path} for video {path}")
            click.echo(f"Created {target_path} for video {path}")


@click.command(options_metavar="<options>")
@click.argument(
    "path",
    type=click.Path(dir_okay=True, exists=True),
    metavar="<path>",
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
@spinner("translate")
def translate(path: str, api_key: str, language: str) -> None:
    """
    The translate command, translates either a single SRT file or files or directory of SRT files into the wanted language.
    """
    logger.info("Starting transcription")

    translator = initiate_client(api_key=api_key)

    path_is_file = os.path.isfile(path)
    path_is_directory = os.path.isdir(path)

    if not path_is_directory and not path_is_file:
        logger.info("Please provide a file or directory")
        exit(1)

    translate_to_languages: list[Languages] = parse_languages(language)

    logger.info(
        f"Translating to following language/languages: {' '.join([language.value for language in translate_to_languages])}"
    )

    files: list[File] = []
    if path_is_file:
        logger.info(f"Adding file {path} for translation")

        for target_language in translate_to_languages:
            logger.info(
                f"Adding file {path} with {target_language.value} for translation"
            )

            target_path = get_new_file_path(path, target_language)

            (contents, breakpoints) = chunk_content(path)

            files.append(
                File(
                    name=path,
                    language=target_language,
                    SRTParts=contents,
                    breakpoints=breakpoints,
                    target_path=target_path,
                    source_path=path,
                )
            )

    if path_is_directory:
        directory_file_paths = get_files_in_directory(path)

        num_of_file_paths = len(directory_file_paths)

        if num_of_file_paths == 1:
            logger.info(f"Processing {num_of_file_paths} file in directory {path}")
        else:
            logger.info(f"Processing {num_of_file_paths} files in directory {path}")

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
        logger.info(f"Created file {target_file.target_path}")
