import logging
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Final

from animotion.domain.camera import Camera
from animotion.domain.event_handler.event_handler import EventHandler

_LOGGER: Final = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class VideoRecorder(EventHandler):
    camera: Camera
    target: Path

    def __post_init__(self) -> None:
        self.target.mkdir(parents=True, exist_ok=True)

    def enter(self) -> None:
        target = self.target / datetime.now().isoformat()
        _LOGGER.info(f"Recording video to {target}")
        self.camera.start_video(target)

    def step(self) -> None:
        pass

    def exit(self) -> None:
        self.camera.stop_video()
