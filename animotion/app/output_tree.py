#!/usr/bin/env python3
from pathlib import Path
from typing import Final

import typer

_FIRST_SEQUENCE_NUMBER: Final[int] = 0
_INSTANCE_FOLDER_NAME_PATTERN: Final[str] = "{:05d}"


def main() -> None:
    typer.run(_main)


def _main(root_folder: Path) -> None:
    print(_next_folder_in_sequence_in(root_folder))


def _next_folder_in_sequence_in(root_folder: Path) -> Path:
    highest_sequence_number = (
        max(
            (
                sequence_number
                for entry in root_folder.iterdir()
                if (sequence_number := _sequence_number_from(entry)) is not None
            ),
            default=_FIRST_SEQUENCE_NUMBER,
        )
        if root_folder.exists()
        else _FIRST_SEQUENCE_NUMBER
    )
    return root_folder / _INSTANCE_FOLDER_NAME_PATTERN.format(
        highest_sequence_number + 1
    )


def _sequence_number_from(path: Path) -> int | None:
    try:
        return int(path.name)
    except ValueError:
        return None


if __name__ == "__main__":
    main()
