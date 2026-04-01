from pathlib import Path
from typing import Final

DEFAULT_CONFIGURATION_PATH: Final[Path] = (
    Path(__file__).parent.resolve() / "default.yml"
)
