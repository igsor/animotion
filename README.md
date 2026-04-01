
# Animotion

This repository is part of a wildlife monitoring project.
It uses the Raspberry Pi camera module to record videos.
Recording is governed by detected motion.


## Installation

Clone from the git repository:

    $ git clone https://github.com/igsor/animotion
    $ cd animotion

Install extra dependencies (debian):

    $ sudo ./install_non_python_packages.sh

Set up a virtual environment:

    $ virtualenv .venv --system-site-packages
    $ source .venv/bin/activate
    $ pip install poetry

Install animotion:

    $ poetry sync

To ensure code style discipline, run the following commands:

    $ bash lint.sh

To see test coverage, run (after the above!)

    $ xdg-open .htmlcov/index.html

To build the package, do:

    $ python -m build
