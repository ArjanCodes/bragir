from pydub import AudioSegment

def combine(objects: list[AudioSegment]) -> AudioSegment | None:
    if len(objects) > 1:
        combined_no_crossfade = objects[0]
        for segment in objects[1:]:
            combined_no_crossfade = combined_no_crossfade.append(segment, crossfade=0)
        return combined_no_crossfade

    if len(objects) == 1:
        return objects[0]

    return None


def group_objects(
    objects: list[AudioSegment], duration_limit_miliseconds: float
) -> list[AudioSegment]:
    duration_limit_seconds = duration_limit_miliseconds / 1000

    # If there is no objects in the list
    if len(objects) == 0:
        return []
    
    # If AudioSegments are less than the limit
    if combine(objects).duration_seconds < duration_limit_seconds:
        return [combine(objects)]

    grouped_objects: list[AudioSegment] = []
    current_group: list[AudioSegment] = []

    total_duration = 0.0
    for obj in objects:
        if total_duration + obj.duration_seconds > duration_limit_seconds:
            combined_no_crossfade = combine(current_group)
            grouped_objects.append(combined_no_crossfade)
            current_group = []
            total_duration = 0.0

        current_group.append(obj)
        total_duration += obj.duration_seconds

    # Add the last group if it contains any objects
    if len(current_group) > 0:
        combined_no_crossfade = current_group[0]
        for segment in current_group[1:]:
            combined_no_crossfade = combined_no_crossfade.append(segment, crossfade=0)

        grouped_objects.append(combined_no_crossfade)

    return grouped_objects
