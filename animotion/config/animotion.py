from dependency_injector import containers, providers

from animotion.config import DEFAULT_CONFIGURATION_PATH
from animotion.config.camera import CameraContainer
from animotion.config.event_handler import EventHandlerContainer
from animotion.config.logging import LoggingContainer
from animotion.config.state_machine import StateMachineContainer
from animotion.config.trigger import TriggerContainer


class AnimotionContainer(containers.DeclarativeContainer):
    config = providers.Configuration(yaml_files=[DEFAULT_CONFIGURATION_PATH])

    logging = providers.Container(LoggingContainer, config=config.logging)

    camera = providers.Container(
        CameraContainer,
        config=config.camera,
    )

    trigger = providers.Container(
        TriggerContainer,
        config=config.trigger,
        camera=camera,
    )

    event_handler = providers.Container(
        EventHandlerContainer,
        config=config,
        camera=camera,
    )

    state_machine = providers.Container(
        StateMachineContainer,
        config=config,
        camera=camera,
        event_handler=event_handler,
        trigger=trigger,
    )
