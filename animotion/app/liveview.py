#!/usr/bin/env python3
from pathlib import Path
from typing import Final

import typer
from flask import Flask, send_file

_DEFAULT_HOST: Final[str] = "0.0.0.0"
_DEFAULT_PORT: Final[int] = 5000
_MAIN_PAGE: Final[str] = """
<!DOCTYPE html>
<html>

<head>
  <title>Livestream</title>
  <meta http-equiv="refresh" content="2">
</head>

<body>
  <img src="/latest.jpg" style="max-height: 100%; max-width: 100%; height: auto; width: auto;"/>
</body>

</html>
"""


def main() -> None:
    typer.run(_main)


def _main(
    image_dump_folder: Path,
    host: str = _DEFAULT_HOST,
    port: int = _DEFAULT_PORT,
    debug: bool = False,
) -> None:
    app = Flask(__name__)

    @app.route("/")
    def landing() -> None:
        return _MAIN_PAGE

    @app.route("/latest.jpg")
    def latest_image() -> None:
        return send_file(max(image_dump_folder.iterdir()), mimetype="image/jpg")

    app.run(
        host=host,
        port=port,
        debug=debug,
    )


if __name__ == "__main__":
    main()
