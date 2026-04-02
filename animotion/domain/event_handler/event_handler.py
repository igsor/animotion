from abc import ABC, abstractmethod


class EventHandler(ABC):
    @abstractmethod
    def enter(self) -> None:
        pass

    @abstractmethod
    def step(self) -> None:
        pass

    @abstractmethod
    def exit(self) -> None:
        pass
