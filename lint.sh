#!/usr/bin/env sh

poetry check \
    && poetry run ruff check --select I animotion tests \
    && poetry run ruff check animotion tests \
    && poetry run mypy \
    && poetry run coverage run \
    && poetry run coverage html
