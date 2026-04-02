from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum, auto
from pathlib import Path
from typing import Final

from PIL import Image
from typing_extensions import assert_never

from animotion.domain.camera import Camera
from animotion.domain.event_handler.event_handler import EventHandler

_LOGGER: Final = logging.getLogger(__name__)


class ImageFormat(Enum):
    JPEG = auto()
    PNG = auto()
    TIFF = auto()

    @staticmethod
    def from_(format: str) -> ImageFormat:
        match format.lower():
            case "jpg" | "jpeg":
                return ImageFormat.JPEG
            case "png":
                return ImageFormat.PNG
            case "tiff":
                return ImageFormat.TIFF
            case _:
                raise ValueError(f"unsupported image format: {format}")


@dataclass
class ImageRecorder(EventHandler):
    camera: Camera
    target: Path
    format: ImageFormat
    interval: timedelta

    _last_capture_time: datetime = field(default=datetime.min)

    def __post_init__(self) -> None:
        self.target.mkdir(parents=True, exist_ok=True)

    def enter(self) -> None:
        pass

    def step(self) -> None:
        now = datetime.now()
        if now - self._last_capture_time > self.interval:
            target = self.target / (now.isoformat() + self._suffix)
            image = Image.fromarray(self.camera.get_high_resolution_image()).convert(
                "RGB"
            )
            image.save(target)
            _LOGGER.info(f"Saving image to {target}")
            self._last_capture_time = now

    def exit(self) -> None:
        pass

    @property
    def _suffix(self) -> str:
        match self.format:
            case ImageFormat.JPEG:
                return ".jpg"
            case ImageFormat.PNG:
                return ".png"
            case ImageFormat.TIFF:
                return ".tiff"
            case _:
                assert_never(self.format)
