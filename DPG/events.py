"""Simple event system (key-driven or random)."""

from typing import Callable, Dict, List, Optional
import random


class Event:
    """Represents a game event that can be triggered."""

    def __init__(self, name: str, description: str, action: Callable[[], None], key: Optional[str] = None):
        self.name = name
        self.description = description
        self.action = action
        self.key = key

    def trigger(self) -> None:
        self.action()


# registry of known events
events: List[Event] = []


def register_event(ev: Event) -> None:
    events.append(ev)


def trigger_key(key: str) -> bool:
    """Trigger the first event matching ``key``; return True if fired."""
    for ev in events:
        if ev.key == key:
            ev.trigger()
            return True
    return False


def trigger_random(chance: float = 0.1) -> Optional[Event]:
    """With probability ``chance`` choose a random event and fire it."""
    if random.random() < chance and events:
        ev = random.choice(events)
        ev.trigger()
        return ev
    return None
