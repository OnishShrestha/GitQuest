
import json
from datetime import date
from pathlib import Path

from bosses import random_boss

ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = ROOT / "data" / "game.json"


def ordinal(number):
    """Convert a number to its ordinal form: 1st, 2nd, 3rd, 4th, etc."""
    if 10 <= number % 100 <= 20:
        suffix = "th"
    else:
        suffix = {
            1: "st",
            2: "nd",
            3: "rd"
        }.get(number % 10, "th")

    return f"{number}{suffix}"


def load_game():
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def save_game(game):
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(game, file, indent=2, ensure_ascii=False)


def get_current_week():
    today = date.today()
    year, week, _ = today.isocalendar()
    return f"{year}-W{week:02d}"


def start_new_week():
    game = load_game()

    current_week = get_current_week()
    previous_week = game.get("boss_week")
    current_boss = game.get("boss")

    print(f"Current week: {current_week}")
    print(f"Previous week: {previous_week}")

    # Do not create another boss if one is already assigned this week.
    if previous_week == current_week and current_boss:
        print(f"\n🐉 Weekly boss already set: {current_boss['name']}")

        generation = current_boss.get("generation", 1)
        print(f"Generation: {ordinal(generation)}")
        print(
            f"HP: {current_boss['hp']}/"
            f"{current_boss['max_hp']}"
        )
        return

    # Display the previous boss status.
    if current_boss:
        if current_boss.get("defeated") or current_boss.get("hp", 1) <= 0:
            print(f"💀 Previous boss defeated: {current_boss['name']}")
        else:
            print(f"🐉 Previous boss survived: {current_boss['name']}")

    # Generate the next boss.
    new_boss = random_boss()
    boss_name = new_boss["name"]

    # Track generations independently for each boss type.
    generations = game.setdefault("boss_generations", {})

    generation = generations.get(boss_name, 0) + 1
    generations[boss_name] = generation

    new_boss["generation"] = generation
    new_boss["generation_label"] = ordinal(generation)

    # Assign the new weekly boss.
    game["boss"] = new_boss
    game["boss_week"] = current_week

    # Reset weekly boss damage.
    game.setdefault("stats", {})
    game["stats"]["boss_damage"] = 0

    # Preserve boss history and achievements if they do not exist yet.
    game.setdefault("boss_history", [])
    game.setdefault("achievements", [])

    save_game(game)

    print("\n🐉 NEW WEEKLY BOSS 🐉")
    print(f"Boss: {new_boss['name']}")
    print(f"Generation: {new_boss['generation_label']} Generation")
    print(f"HP: {new_boss['hp']}/{new_boss['max_hp']}")
    print(f"Week: {current_week}")


if __name__ == "__main__":
    start_new_week()
