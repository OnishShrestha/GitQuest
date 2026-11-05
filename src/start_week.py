
import json
from datetime import date
from pathlib import Path

from bosses import random_boss

ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = ROOT / "data" / "game.json"


def start_new_week():
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        game = json.load(file)

    today = date.today()
    year, week, _ = today.isocalendar()
    current_week = f"{year}-W{week:02d}"

    previous_week = game.get("boss_week")

    if previous_week == current_week:
        print(f"Weekly boss already set for {current_week}.")
        return

    new_boss = random_boss()

    game["boss"] = new_boss
    game["boss_week"] = current_week

    game.setdefault("stats", {})
    game["stats"]["boss_damage"] = 0

    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(game, file, indent=2, ensure_ascii=False)

    print(f"New weekly boss: {new_boss['name']}")
    print(f"Week: {current_week}")


if __name__ == "__main__":
    start_new_week()
