from dataclasses import dataclass, field
from pathlib import Path
from random import random

import numpy as np
from numpy import typing as npt

from animotion.domain.camera import Camera


@dataclass
class Null(Camera):
    resolution: tuple[int, int] = field(default=(320, 240))
    preview_switch_threshold: float = field(default=0.9)

    _last_image: npt.NDArray = field(init=False)

    def __post_init__(self) -> None:
        self._last_image = np.random.random(self.resolution)

    def get_low_resolution_image(self) -> npt.NDArray:
        if random() > self.preview_switch_threshold:
            self._last_image = np.random.random(self.resolution)
        return self._last_image

    def get_high_resolution_image(self) -> npt.NDArray:
        return np.random.random(self.resolution)

    def start_video(self, path: Path) -> None:
        pass

    def stop_video(self) -> None:
        pass
