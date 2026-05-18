from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Callable, Optional

from . import level


@dataclass
class Experience:
    """Simple experience tracker and level-up manager.

    Attributes
    ----------
    current : int
        The current accumulated experience points.
    to_level : int
        Experience required to reach the next level.
    scale : float
        Factor to multiply ``to_level`` by after each level-up.
    on_level_up : Optional[Callable[[int], None]]
        Optional callback invoked with the number of levels gained whenever
        ``current`` exceeds ``to_level``. This can be used by the UI layer to
        react to level changes.
    """

    current: int = 0
    to_level: int = 100
    scale: float = 1.0  # add a flat amount by default
    on_level_up: Optional[Callable[[int], None]] = None

    def add(self, amount: int) -> None:
        """Add experience points and perform any resulting level-ups.

        Parameters
        ----------
        amount : int
            Amount of experience to add (must be non-negative).
        """
        if amount < 0:
            raise ValueError("cannot add negative experience")

        self.current += amount
        self._check_level_up()

    def _check_level_up(self) -> None:
        """Internal helper that levels the player repeatedly as needed."""
        levels_gained = 0
        # determine how many thresholds we pass
        while self.current >= self.to_level:
            self.current -= self.to_level
            levels_gained += 1
            # bump the threshold for the *next* check
            if self.scale > 1:
                self.to_level = int(self.to_level * self.scale)
            else:
                self.to_level += int(self.scale)

        if levels_gained:
            # perform all level changes in one call
            level.level_up(levels_gained)
            if self.on_level_up:
                self.on_level_up(levels_gained)

    def reset(self) -> None:
        """Return the experience tracker to its initial state."""
        self.current = 0
        self.to_level = 100
        self.scale = 1.0

    @property
    def remaining(self) -> int:
        """Experience needed until the next level."""
        return max(0, self.to_level - self.current)

    @property
    def percent(self) -> float:
        """Fraction (0.0–1.0) of progress toward the next level."""
        if self.to_level == 0:
            return 0.0
        return self.current / self.to_level

    def to_dict(self) -> dict:
        """Return a serialisable dictionary for saving."""
        return asdict(self)

    def load_dict(self, data: dict) -> None:
        """Load values from a dictionary (e.g. when loading a game)."""
        self.current = data.get("current", self.current)
        self.to_level = data.get("to_level", self.to_level)
        self.scale = data.get("scale", self.scale)


# module‑level singleton for legacy convenience
xp = Experience()


# backwards compatible helpers

def add_exp(amount: int) -> None:
    """Add experience to the shared tracker."""
    xp.add(amount)


def check_level_up() -> None:
    """Legacy wrapper; ``add_exp`` already calls this automatically."""
    xp._check_level_up()  # pragma: no cover
    