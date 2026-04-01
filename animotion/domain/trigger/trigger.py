from abc import ABC, abstractmethod

from animotion.domain.state import State


class Trigger(ABC):
    @abstractmethod
    def get_next_state(self, current: State) -> State:
        pass
