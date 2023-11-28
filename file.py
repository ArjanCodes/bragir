import click
from constants import TOKEN_LIMIT
from path_components import File, SRTPart


def read_file(file_path: str):
    with open(file_path, "r") as file:
        file_content = file.read()
    return file_content


def create_translation_file(file: File, content: str):
    with open(file.target_path, "a+", encoding="utf-8") as fileIO:
        fileIO.write(content)

def chunk_content(file_path: str) -> tuple[list[SRTPart], list[int]]:
    buffer_limit: int = TOKEN_LIMIT
    buffer = 0

    breakpoints: list[int] = []

    file_content = read_file(file_path)

    subtitle_blocks = file_content.strip().split("\n\n")

    SRTParts: list[SRTPart] = []
    for block in subtitle_blocks:
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

    for i, strpart in enumerate(SRTParts):
        buffer += strpart.number_of_tokens

        if buffer > buffer_limit:
            prev_srt_part = SRTParts[i - 1]
            next_srt_part = strpart

            click.echo(
                f"Chunking at between {prev_srt_part.index} and {next_srt_part.index}"
            )
            breakpoints.append(i)

            sentences: list[str] = prev_srt_part.content.split(".")

            last_sentence = sentences[-1]

            prev_srt_part.content = "".join(prev_srt_part.content.split(".")[:-1])

            next_srt_part.content = last_sentence + " " + next_srt_part.content

            buffer = 0

    return (SRTParts, breakpoints)