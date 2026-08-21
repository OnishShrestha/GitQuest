import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parent.parent / "src")
)

from game import level_for_xp
from bosses import random_boss
from events import random_event


def test_level_system():
    assert level_for_xp(0) == 1
    assert level_for_xp(100) == 2
    assert level_for_xp(500) == 6


def test_boss():
    boss = random_boss()

    assert boss["hp"] == boss["max_hp"]
    assert boss["defeated"] is False


def test_event():
    event = random_event()

    assert "name" in event
    assert "xp" in event
    assert "gold" in event