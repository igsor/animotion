
# Animotion

The Black Star File System (BSFS) is a semantic file system, meaning that it organizes files
by association, and can record files, their metadata and content in a structured manner.


## Installation

Clone from the git repository:

    $ git clone https://github.com/igsor/animotion
    $ cd animotion

Set up a virtual environment:

    $ virtualenv .venv
    $ source .venv/bin/activate
    $ pip install poetry

Install bsfs:

    $ poetry sync

To ensure code style discipline, run the following commands:

    $ bash lint.sh

To see test coverage, run (after the above!)

    $ xdg-open .htmlcov/index.html

To build the package, do:

    $ python -m build
