"""Simple quest tracking infrastructure."""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Dict


@dataclass
class Quest:
    id: str
    description: str
    objectives: List[str]
    rewards: Dict[str, int] = field(default_factory=dict)  # e.g. gold, exp
    completed: bool = False

    def check_complete(self, achieved: List[str]) -> bool:
        """Mark quest complete if all objectives achieved.

        Objectives beginning with ``kill_`` are treated specially; the
        requirements are checked against the player's kill counts tracked in
        ``DPG.user``.  Other objectives are matched against the ``achieved``
        list provided by the caller.
        """
        from . import user

        for obj in self.objectives:
            if obj.startswith("kill_"):
                # expected format kill_<monster>_<count>
                parts = obj.split("_")
                if len(parts) >= 3:
                    monster = parts[1]
                    try:
                        needed = int(parts[2])
                    except ValueError:
                        needed = 0
                    if user.get_kills(monster) < needed:
                        return False
            elif obj.startswith("have_"):
                # expected have_<item>_<count>
                parts = obj.split("_")
                if len(parts) >= 3:
                    item_name = parts[1]
                    try:
                        needed = int(parts[2])
                    except ValueError:
                        needed = 0
                    # count inventory occurrences
                    from . import inventory
                    qty = sum(e['quantity'] for e in inventory.inventory_list if e['name'] == item_name)
                    if qty < needed:
                        return False
            else:
                if obj not in achieved:
                    return False
        self.completed = True
        return self.completed


# registry
quests: Dict[str, Quest] = {}
active: List[Quest] = []


def register_quest(q: Quest) -> None:
    quests[q.id] = q


def start_quest(qid: str) -> bool:
    q = quests.get(qid)
    if q and q not in active:
        active.append(q)
        return True
    return False


def complete_quest(qid: str, achieved: List[str]) -> bool:
    q = next((qq for qq in active if qq.id == qid), None)
    if q and q.check_complete(achieved):
        active.remove(q)
        return True
    return False


def get_active() -> List[Quest]:
    return list(active)


def register_guild_quest(qid: str, monster: str, count: int, rewards: Dict[str, int]) -> None:
    """Convenience for registering a kill-x quest from the guild.

    ``qid`` is the unique identifier; ``monster`` and ``count`` describe the
    target.  The objectives string is formatted to be handled by
    ``check_complete``.  ``rewards`` is passed straight through to the quest
    constructor, so the caller may request gold, exp, etc.
    """
    desc = f"Hunt {count} {monster}(s) for the guild"
    obj = [f"kill_{monster}_{count}"]
    register_quest(Quest(qid, desc, obj, rewards=rewards))


def get_hint(qid: str) -> str:
    """Return a human-friendly hint for the given quest ID.

    This simply echoes the description along with a gentle reminder of the
    first objective.  Consumers can display this to the player when they
    request help.
    """
    q = quests.get(qid)
    if not q:
        return "No such quest."
    # build a simple hint, avoid exposing raw objective keys if possible
    hint = q.description
    if q.objectives:
        hint += " (try to " + q.objectives[0].replace('_', ' ') + ")"
    return hint
