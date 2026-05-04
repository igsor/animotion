from pathlib import Path
from typing import Final

_INSTANCE_FOLDER_NAME_PATTERN: Final[str] = "{:05d}"


def next_folder_in_sequence_in(root_folder: Path) -> Path:
    highest_sequence_number = (
        max(
            (
                sequence_number
                for entry in root_folder.iterdir()
                if (sequence_number := _sequence_number_from(entry)) is not None
            ),
            default=0,
        )
        if root_folder.exists()
        else 0
    )
    return root_folder / _INSTANCE_FOLDER_NAME_PATTERN.format(
        highest_sequence_number + 1
    )


def _sequence_number_from(path: Path) -> int | None:
    try:
        return int(path.name)
    except ValueError:
        return None
