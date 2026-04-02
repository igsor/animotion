from pathlib import Path

from dependency_injector import containers, providers

from animotion.domain.event_handler.noop import Noop
from animotion.domain.event_handler.video_recorder import VideoRecorder


class EventHandlerContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    camera = providers.DependenciesContainer()

    noop = providers.Factory(Noop)

    _video_recorder_target = providers.Factory(Path, config.app.video_target_folder)

    video_recorder = providers.Factory(
        VideoRecorder,
        camera=camera.camera,
        target=_video_recorder_target,
    )
