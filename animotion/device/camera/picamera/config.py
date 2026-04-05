from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class VideoConfig:
    resolution: tuple[int, int]
    format: str  # RGB888, BGR888, XBGR8888, XRGB8888, YUV420
    encoder: str  # H264, JPEG, MJPEG, NULL
    bitrate: int
    quality: str  # VERY_LOW, LOW, MEDIUM, HIGH, VERY_HIGH


@dataclass(frozen=True, slots=True)
class PreviewConfig:
    resolution: tuple[int, int]
    format: str


@dataclass(frozen=True, slots=True)
class Config:
    video: VideoConfig
    preview: PreviewConfig
    horizontal_flip: bool
    vertical_flip: bool
