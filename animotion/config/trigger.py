from dependency_injector import containers, providers

from animotion.domain.trigger.difference import PixelDifference
from animotion.domain.trigger.time import DelayedWait


class TriggerContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    camera = providers.DependenciesContainer()

    _difference_trigger = providers.Factory(
        PixelDifference,
        camera=camera.camera,
        threshold=config.threshold,
    )

    trigger = providers.Factory(
        DelayedWait,
        trigger=_difference_trigger,
        delay_in_seconds=config.delay_in_seconds,
    )
