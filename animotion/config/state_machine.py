from dependency_injector import containers, providers

from animotion.domain.state_machine import StateMachine


class StateMachineContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    camera = providers.DependenciesContainer()
    event_handler = providers.DependenciesContainer()
    trigger = providers.DependenciesContainer()

    state_machine = providers.Factory(
        StateMachine,
        trigger=trigger.trigger,
        on_wait=event_handler.image_recorder,
        on_observe=event_handler.video_recorder,
    )
