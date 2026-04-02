#!/usr/bin/env python3
from pathlib import Path

import typer
from dependency_injector.providers import Configuration
from dependency_injector.wiring import Provide, inject

from animotion.config.animotion import AnimotionContainer
from animotion.domain.state_machine import StateMachine


def main() -> None:
    typer.run(_main)


def _main(
    output_folder: Path | None = None,
    config_file: Path | None = None,
) -> None:
    _init(
        output_folder=output_folder,
        config_file=config_file,
    )
    _run()


def _init(
    output_folder: Path | None = None,
    config_file: Path | None = None,
) -> None:
    app = AnimotionContainer()
    if config_file is not None:
        _load_config_from_path(app.config, config_file)
    if output_folder is not None:
        app.config.app.video_target_folder.from_value(output_folder)
    app.logging.init_resources()
    app.wire(modules=[__name__])


def _load_config_from_path(config: Configuration, path: Path) -> None:
    match path.suffix:
        case ".yml":
            config.from_yaml(path)
        case ".json":
            config.from_json(path)
        case ".ini":
            config.from_ini(path)
        case _:
            raise ValueError(path.suffix)


@inject
def _run(
    app: StateMachine = Provide[AnimotionContainer.state_machine.state_machine],
) -> None:
    app.run()


if __name__ == "__main__":
    main()
