from pathlib import Path

from dependency_injector import containers, providers

from animotion.domain.event_handler.noop import Noop
from animotion.domain.event_handler.video_recorder import VideoRecorder
from animotion.domain.state_machine import StateMachine


class StateMachineContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    camera = providers.DependenciesContainer()
    trigger = providers.DependenciesContainer()

    on_wait = providers.Factory(Noop)

    _target = providers.Factory(Path, config.app.video_target_path)

    on_observe = providers.Factory(
        VideoRecorder,
        camera=camera.camera,
        target=_target,
    )

    state_machine = providers.Factory(
        StateMachine,
        trigger=trigger.trigger,
        on_wait=on_wait,
        on_observe=on_observe,
    )
