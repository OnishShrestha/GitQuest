import json
from datetime import date
from pathlib import Path

from bosses import random_boss


ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = ROOT / "data" / "game.json"


def load_game():
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def save_game(game):
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(game, file, indent=2)


def get_week_id():
    today = date.today()

    year, week, _ = today.isocalendar()

    return f"{year}-W{week:02d}"


def start_new_week():
    game = load_game()

    current_week = get_week_id()

    previous_week = game.get("boss_week")

    # Prevent the boss from being reset multiple times
    # during the same week.
    if previous_week == current_week:
        print(
            f"🐉 Weekly boss already set for {current_week}."
        )
        print(
            f"Current boss: {game['boss']['name']}"
        )
        print(
            f"HP: {game['boss']['hp']}/"
            f"{game['boss']['max_hp']}"
        )

        return

    # If there was a previous boss, record the result.
    if game.get("boss"):

        old_boss = game["boss"]

        if old_boss.get("defeated"):
            print(
                f"💀 Previous boss defeated: "
                f"{old_boss['name']}"
            )
        else:
            print(
                f"🐉 Previous boss survived: "
                f"{old_boss['name']}"
            )

    # Create a new random boss.
    new_boss = random_boss()

    game["boss"] = new_boss

    # Remember which week this boss belongs to.
    game["boss_week"] = current_week

    # Reset weekly boss damage.
    game["stats"]["boss_damage"] = 0

    save_game(game)

    print()
    print("╔════════════════════════════════════╗")
    print("║       🐉 NEW WEEKLY BOSS 🐉        ║")
    print("╚════════════════════════════════════╝")
    print()

    print(f"Boss: {new_boss['name']}")
    print(f"HP: {new_boss['hp']}")
    print(f"Week: {current_week}")
    print()

    print("⚔️ The adventure begins!")
    print()


if __name__ == "__main__":
    start_new_week()