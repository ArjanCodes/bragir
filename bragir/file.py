import os

import click
from bragir.constants import TOKEN_LIMIT
from bragir.languages import Languages
from bragir.path_components import File, SRTPart
from bragir.transcriber import chunk_audio


def calculate_file_size(file_path: str) -> float:
    file_size_bytes = os.path.getsize(file_path)
    return file_size_bytes / (1024 * 1024)


def read_file(file_path: str):
    with open(file_path, "r") as file:
        file_content = file.read()
    return file_content


def create_file(file: File, content: str):
    with open(file.target_path, "a+", encoding="utf-8") as fileIO:
        fileIO.write(content)


def chunk_content_into_srt_parts(content: str) -> list[SRTPart]:
    blocks = content.strip().split("\n\n")

    SRTParts: list[SRTPart] = []
    for block in blocks:
        lines = block.split("\n")

        number = int(lines[0])
        times = lines[1].split(" --> ")
        start_time, end_time = times[0], times[1]
        text = " ".join(lines[2:])

        SRTParts.append(
            SRTPart(
                index=number,
                start_time=start_time,
                end_time=end_time,
                content=text,
                source=block,
            )
        )

    return SRTParts


def get_breakpoints(SRTParts: list[SRTPart]) -> list[int]:
    buffer_limit: int = TOKEN_LIMIT
    buffer = 0

    breakpoints: list[int] = []

    for i, strpart in enumerate(SRTParts):
        buffer += strpart.number_of_tokens

        if buffer > buffer_limit:
            prev_srt_part = SRTParts[i - 1]
            next_srt_part = strpart

            breakpoints.append(i)

            sentences: list[str] = prev_srt_part.content.split(".")

            last_sentence = sentences[-1]

            prev_srt_part.content = "".join(prev_srt_part.content.split(".")[:-1])

            next_srt_part.content = last_sentence + " " + next_srt_part.content

            buffer = 0

    return breakpoints


def chunk_content(file_path: str) -> tuple[list[SRTPart], list[int]]:
    file_content = read_file(file_path)

    SRTParts: list[SRTPart] = chunk_content_into_srt_parts(file_content)

    breakpoints: list[int] = get_breakpoints(SRTParts)

    return (SRTParts, breakpoints)


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


def process_file(file_path: str) -> list[str]:
    chunks = chunk_audio(file_path)
    directory, base_name = os.path.split(file_path)

    chunk_paths: list[str] = []
    for i, chunk in enumerate(chunks):
        new_base_name = f"{i}_{base_name}"
        new_path = os.path.join(directory, new_base_name)
        chunk.export(new_path, format="mp3")
        chunk_paths.append(new_path)  # type:ignore

    return chunk_paths


def remove_files(file_paths: list[str]):
    click.echo("Starting cleanup process...")
    for path in file_paths:
        if not os.path.exists(path):
            click.echo(f"File {path} not found. Skipping.")
            continue

        try:
            os.remove(path)
            click.echo(f"File {path} has been successfully removed.")
        except PermissionError as e:
            raise click.ClickException(f"Permission denied while trying to remove {path}: {e}")
        except Exception as e:
            raise click.ClickException(f"Error removing file {path}: {e}")
