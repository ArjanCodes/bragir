from typing import Any


def split_list_at_breakpoints(original_list: list[Any], breakpoints: list[int]):
    result: list[Any] = []
    start_index = 0

    for breakpoint in breakpoints:
        result.append(original_list[start_index:breakpoint])
        start_index = breakpoint

    # Append the remaining elements after the last breakpoint
    result.append(original_list[start_index:])

    return result