import logging
from dataclasses import dataclass
from typing import Final

from animotion.domain.event_handler.event_handler import EventHandler
from animotion.domain.state import State
from animotion.domain.trigger.trigger import Trigger

_LOGGER: Final = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class StateMachine:
    trigger: Trigger
    on_wait: EventHandler
    on_observe: EventHandler

    def run(self, current_state: State = State.WAIT) -> None:
        while True:
            next_state = self.trigger.get_next_state(current_state)
            self._handle_state_transition(current_state, next_state)
            current_state = next_state

    def _handle_state_transition(self, current_state: State, next_state: State) -> None:
        if current_state != next_state:
            _LOGGER.info(f"state transition from {current_state} to {next_state}")
        match (current_state, next_state):
            case (State.WAIT, State.WAIT):
                self.on_wait.step()
            case (State.WAIT, State.OBSERVE):
                self.on_wait.exit()
                self.on_observe.enter()
            case (State.OBSERVE, State.OBSERVE):
                self.on_observe.step()
            case (State.OBSERVE, State.WAIT):
                self.on_observe.exit()
                self.on_wait.enter()
            case _:
                raise AssertionError("uncovered state combination")
