import logging
from dataclasses import dataclass, field
from time import time
from typing import Final

from animotion.domain.state import State
from animotion.domain.trigger.trigger import Trigger

_LOGGER: Final = logging.getLogger(__name__)


@dataclass
class EnsureObserveDuration(Trigger):
    trigger: Trigger
    duration_in_seconds: float

    _switched_to_observe: float = field(default_factory=time)

    def get_next_state(self, current: State) -> State:
        proposed = self.trigger.get_next_state(current)
        match current, proposed:
            case (State.OBSERVE, State.WAIT):
                return (
                    State.WAIT
                    if (self._switched_to_observe + self.duration_in_seconds <= time())
                    else State.OBSERVE
                )
            case (State.WAIT, State.OBSERVE):
                self._switched_to_observe = time()
                return proposed
            case _:
                return proposed


@dataclass
class DelayedWait(Trigger):
    trigger: Trigger
    delay_in_seconds: float

    _transition_first_triggered: float | None = field(default=None)

    def get_next_state(self, current: State) -> State:
        proposed = self.trigger.get_next_state(current)
        match current, proposed:
            case (State.OBSERVE, State.WAIT):
                if self._transition_first_triggered is None:
                    _LOGGER.debug(
                        f"Start {self.delay_in_seconds} seconds timer before transitioning to WAIT"
                    )
                    self._transition_first_triggered = time()
                    return State.OBSERVE
                return (
                    State.WAIT
                    if self._transition_first_triggered + self.delay_in_seconds
                    <= time()
                    else State.OBSERVE
                )
            case _:
                self._transition_first_triggered = None
                return proposed
