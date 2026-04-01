from dataclasses import dataclass

from animotion.domain.event_handler.event_handler import EventHandler


@dataclass(frozen=True, slots=True)
class Noop(EventHandler):
    def enter(self) -> None:
        pass

    def exit(self) -> None:
        pass
