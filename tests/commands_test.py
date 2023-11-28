from unittest.mock import MagicMock
from click.testing import CliRunner
from bragir.commands import transcribe, translate
from pydub import AudioSegment


class FakeClient:
    def __init__(self):
        self.audio = MagicMock()
        self.audio.transcriptions = MagicMock()

    def set_transcriptions_return_value(self, return_value: list[str]):
        self.audio.transcriptions.return_value = return_value


def create_test_segment(duration_ms: int) -> AudioSegment:
    # Helper function to create a test AudioSegment of a given duration
    return AudioSegment.silent(duration=duration_ms)


def test_transcribe_help():
    runner = CliRunner()
    result = runner.invoke(transcribe, ["--help"])
    assert result.exit_code == 0


def test_translate_help():
    runner = CliRunner()
    result = runner.invoke(translate, ["--help"])
    assert result.exit_code == 0


def test_transcribe():
    runner = CliRunner()

    with runner.isolated_filesystem():
        audio_segment = create_test_segment(1000)
        audio_segment.export("test.mp4", format="mp4")  # type: ignore

        result = runner.invoke(transcribe, ["test.mp4"], obj={"client": FakeClient()})
        print(result.output)
