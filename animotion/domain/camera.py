from abc import ABC, abstractmethod
from pathlib import Path

from numpy import typing as npt


class Camera(ABC):
    @abstractmethod
    def get_low_resolution_image(self) -> npt.NDArray:
        pass

    @abstractmethod
    def get_high_resolution_image(self) -> npt.NDArray:
        pass

    @abstractmethod
    def start_video(self, path: Path) -> None:
        pass

    @abstractmethod
    def stop_video(self) -> None:
        pass
