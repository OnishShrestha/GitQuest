
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
    current_boss = game.get("boss")

    print(f"Current week: {current_week}")
    print(f"Previous week: {previous_week}")

    if previous_week == current_week and current_boss:
        print(f"🐉 Weekly boss already set: {current_boss['name']}")
        print(f"HP: {current_boss['hp']}/{current_boss['max_hp']}")
        return

    if current_boss:
        if current_boss.get("defeated"):
            print(f"💀 Previous boss defeated: {current_boss['name']}")
        else:
            print(f"🐉 Previous boss survived: {current_boss['name']}")

    new_boss = random_boss()

    game["boss"] = new_boss
    game["boss_week"] = current_week

    game.setdefault("stats", {})
    game["stats"]["boss_damage"] = 0

    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(game, file, indent=2, ensure_ascii=False)

    print("\n🐉 NEW WEEKLY BOSS 🐉")
    print(f"Boss: {new_boss['name']}")
    print(f"HP: {new_boss['hp']}/{new_boss['max_hp']}")
    print(f"Week: {current_week}")


if __name__ == "__main__":
    start_new_week()
