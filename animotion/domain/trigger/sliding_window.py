from __future__ import annotations

from collections import Counter
from collections.abc import Iterator, Mapping
from dataclasses import dataclass, field
from typing import Generic, TypeVar

from animotion.domain.state import State
from animotion.domain.trigger.trigger import Trigger


@dataclass
class SlidingWindow(Trigger):
    trigger: Trigger
    window_size: int

    _window: _FIFO[State] = field(init=False)

    def __post_init__(self) -> None:
        assert self.window_size > 0, "window size must be greater than zero"
        self._window = _FIFO(self.window_size)

    def get_next_state(self, current: State) -> State:
        self._window.put(self.trigger.get_next_state(current))
        return self._argmax(Counter(self._window))

    @staticmethod
    def _argmax(histogram: Mapping[State, int]) -> State:
        return max(histogram, key=histogram.__getitem__)


_T = TypeVar("_T")


@dataclass
class _FIFO(Generic[_T]):
    max_size: int

    _queue: list[_T] = field(default=[], init=False)

    def put(self, element: _T) -> None:
        self._queue.append(element)
        if len(self._queue) > self.max_size:
            self._queue.pop(0)

    def __iter__(self) -> Iterator[_T]:
        return iter(self._queue)
