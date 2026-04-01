#!/usr/bin/env python3

import typer
from dependency_injector.wiring import Provide, inject

from animotion.config.animotion import AnimotionContainer
from animotion.domain.state_machine import StateMachine


def main() -> None:
    typer.run(_main)


def _main() -> None:
    _init()
    _run()


def _init() -> None:
    app = AnimotionContainer()
    app.logging.init_resources()
    app.wire(modules=[__name__])


@inject
def _run(
    app: StateMachine = Provide[AnimotionContainer.state_machine.state_machine],
) -> None:
    app.run()


if __name__ == "__main__":
    main()
