from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from libcamera import Transform
from numpy import typing as npt
from picamera2 import Picamera2
from picamera2.encoders import H264Encoder, JpegEncoder, MJPEGEncoder
from picamera2.encoders.encoder import Encoder
from picamera2.outputs import PyavOutput

from animotion.device.camera.picamera.config import Config, VideoConfig
from animotion.domain.camera import Camera


@dataclass(frozen=True, slots=True)
class PiCamera(Camera):
    _device: Picamera2
    _encoder: Encoder
    _lores_resolution: tuple[int, int]
    _suffix: ClassVar[str] = ".mp4"

    @classmethod
    def from_config(cls, config: Config) -> PiCamera:
        return PiCamera(
            _device=cls._build_device(config),
            _encoder=cls._build_encoder(config.video),
            _lores_resolution=config.preview.resolution,
        )

    @staticmethod
    def _build_device(config: Config) -> None:
        main = {
            "size": config.video.resolution,
            "format": config.video.format,
        }
        lores = {
            "size": config.preview.resolution,
            "format": config.preview.format,
        }
        transform = Transform(
            hflip=False,
            vflip=False,
        )
        device = Picamera2()
        device.configure(
            device.create_video_configuration(
                main,
                lores=lores,
                transform=transform,
            ),
        )

        device.start()
        return device

    @staticmethod
    def _build_encoder(config: VideoConfig) -> None:
        match config.encoder:
            case "H264":
                return H264Encoder(bitrate=config.bitrate)
            case "JPEG":
                return JpegEncoder()
            case "MJPEG":
                return MJPEGEncoder(bitrate=config.bitrate)
            case _:
                raise ValueError(f"invalid encoder choice {config.encoder}")

    def get_low_resolution_image(self) -> npt.NDArray:
        width, height = self._lores_resolution
        return self._device.capture_array("lores")[:height, :width]

    def get_high_resolution_image(self) -> npt.NDArray:
        return self._device.capture_array("main")

    def start_video(self, path: Path) -> None:
        self._encoder.output = PyavOutput(str(path) + self._suffix)
        self._device.start_encoder(self._encoder)

    def stop_video(self) -> None:
        self._device.stop_encoder()
