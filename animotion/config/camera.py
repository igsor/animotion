from dependency_injector import containers, providers

from animotion.device.camera.null.null import Null
from animotion.device.camera.picamera.config import Config, PreviewConfig, VideoConfig
from animotion.device.camera.picamera.picamera import PiCamera


class CameraContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    _video_config = providers.Factory(
        VideoConfig,
        resolution=config.video.resolution,
        format=config.video.format,
        encoder=config.video.encoder,
        bitrate=config.video.bitrate,
        quality=config.video.quality,
    )
    _preview_config = providers.Factory(
        PreviewConfig,
        resolution=config.preview.resolution,
        format=config.preview.format,
    )
    _camera_config = providers.Factory(
        Config,
        video=_video_config,
        preview=_preview_config,
    )
    pi_camera = providers.Singleton(
        PiCamera.from_config,
        config=_camera_config,
    )

    null_camera = providers.Factory(Null)

    camera = pi_camera
