import logging
from dataclasses import dataclass, field
from typing import Final

import numpy as np
import numpy.typing as npt

from animotion.domain.camera import Camera
from animotion.domain.state import State
from animotion.domain.trigger.trigger import Trigger

_LOGGER: Final = logging.getLogger(__name__)


@dataclass
class PixelDifference(Trigger):
    camera: Camera
    threshold: float

    _previous_frame: npt.NDArray = field(init=False)

    def __post_init__(self) -> None:
        self._previous_frame = self.camera.get_low_resolution_image()

    def get_next_state(self, current: State) -> State:
        current_frame = self.camera.get_low_resolution_image()
        difference = np.square(np.subtract(current_frame, self._previous_frame)).mean()
        _LOGGER.debug(f"Difference between frames: {difference}")
        self._previous_frame = current_frame
        return State.WAIT if difference <= self.threshold else State.OBSERVE
