import time
from aurorababel.timer import timing_decorator

def test_decorated_function_with_extra_argument(capsys): # type: ignore

    @timing_decorator
    def example_function_decorated():
        time.sleep(1)

    example_function_decorated()  # type: ignore

    captured = capsys.readouterr() # type: ignore

    # Assert that the expected string is present in the captured output
    assert "example_function_decorated elapsed time:" in captured.out # type: ignore
