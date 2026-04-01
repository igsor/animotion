from collections import Counter
from collections.abc import Mapping, Set
from dataclasses import dataclass

from animotion.domain.state import State
from animotion.domain.trigger.trigger import Trigger


@dataclass(frozen=True, slots=True)
class Ensemble(Trigger):
    triggers: Set[Trigger]

    def get_next_state(self, current: State) -> State:
        return self._argmax(
            Counter((trigger.get_next_state(current) for trigger in self.triggers))
        )

    @staticmethod
    def _argmax(histogram: Mapping[State, int]) -> State:
        return max(histogram, key=histogram.__getitem__)
