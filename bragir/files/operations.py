from bragir.files.file import File


def read_file(file_path: str):
    with open(file_path, "r") as file:
        file_content = file.read()
    return file_content


def create_file(file: File, content: str):
    with open(file.target_path, "a+", encoding="utf-8") as fileIO:
        fileIO.write(content)
