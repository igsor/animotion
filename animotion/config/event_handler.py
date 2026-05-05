from datetime import timedelta
from pathlib import Path

from dependency_injector import containers, providers

from animotion.domain.event_handler.image_recorder import ImageFormat, ImageRecorder
from animotion.domain.event_handler.noop import Noop
from animotion.domain.event_handler.video_recorder import VideoRecorder


class EventHandlerContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    camera = providers.DependenciesContainer()

    noop = providers.Factory(Noop)

    _image_recorder_target = providers.Factory(Path, config.app.image_target_folder)

    _image_recorder_format = providers.Factory(
        ImageFormat.from_, config.app.image_format
    )

    _image_recorder_interval = providers.Factory(
        timedelta, seconds=config.app.image_interval_in_seconds
    )

    image_recorder = providers.Factory(
        ImageRecorder,
        camera=camera.camera,
        target=_image_recorder_target,
        format=_image_recorder_format,
        interval=_image_recorder_interval,
    )

    _video_recorder_target = providers.Factory(Path, config.app.video_target_folder)

    video_recorder = providers.Factory(
        VideoRecorder,
        camera=camera.camera,
        target=_video_recorder_target,
    )
