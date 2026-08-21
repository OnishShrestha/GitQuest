import json
import random
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = ROOT / "data" / "game.json"


def load_game():
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def save_game(game):
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(game, file, indent=2)


def level_for_xp(xp):
    return max(1, xp // 100 + 1)


def add_xp(game, amount):
    player = game["player"]

    old_level = player["level"]

    player["xp"] += amount
    player["level"] = level_for_xp(player["xp"])

    if player["level"] > old_level:
        return f"🎉 Level Up! You reached Level {player['level']}!"

    return None


def choose_daily_event():
    events = [
        {
            "type": "quest",
            "name": "🐛 Defeat the Bug Goblin",
            "description": "Find and resolve a small issue.",
            "xp": 100,
            "gold": 50
        },
        {
            "type": "docs",
            "name": "📚 Restore the Lost Documentation",
            "description": "Improve a section of the project documentation.",
            "xp": 75,
            "gold": 30
        },
        {
            "type": "testing",
            "name": "🛡️ Build the Testing Shield",
            "description": "Add or improve a test.",
            "xp": 100,
            "gold": 40
        },
        {
            "type": "treasure",
            "name": "🎁 Discover Hidden Treasure",
            "description": "Find something useful to improve in the project.",
            "xp": 50,
            "gold": 100
        }
    ]

    return random.choice(events)


def process_day():
    game = load_game()
    player = game["player"]

    today = str(date.today())

    # Prevent duplicate execution on the same day.
    if any(entry["date"] == today for entry in game["history"]):
        print("Today's quest has already been processed.")
        return

    # 75% active / 25% rest day.
    active = random.random() < 0.75

    if not active:
        player["days_skipped"] += 1
        player["streak"] = 0

        game["history"].append({
            "date": today,
            "status": "rest",
            "event": "🌙 Rest Day"
        })

        save_game(game)

        print("🌙 Rest day. No commit required.")
        return

    event = choose_daily_event()

    player["days_active"] += 1
    player["streak"] += 1
    player["quests_completed"] += 1
    player["gold"] += event["gold"]

    level_message = add_xp(game, event["xp"])

    if event["type"] == "docs":
        game["stats"]["docs_improved"] += 1

    elif event["type"] == "testing":
        game["stats"]["tests_added"] += 1

    elif event["type"] == "quest":
        game["stats"]["bugs_defeated"] += 1

    elif event["type"] == "treasure":
        game["stats"]["treasures_found"] += 1

    game["history"].append({
        "date": today,
        "status": "active",
        "event": event["name"],
        "description": event["description"],
        "xp": event["xp"],
        "gold": event["gold"]
    })

    check_achievements(game)

    save_game(game)

    print(event["name"])
    print(event["description"])
    print(f"+{event['xp']} XP")
    print(f"+{event['gold']} Gold")

    if level_message:
        print(level_message)


def check_achievements(game):
    player = game["player"]
    achievements = game["achievements"]

    if player["quests_completed"] >= 1 and "First Quest" not in achievements:
        achievements.append("First Quest")

    if player["quests_completed"] >= 10 and "Quest Master" not in achievements:
        achievements.append("Quest Master")

    if player["quests_completed"] >= 25 and "Elite Adventurer" not in achievements:
        achievements.append("Elite Adventurer")

    if player["streak"] >= 7 and "Seven Day Warrior" not in achievements:
        achievements.append("Seven Day Warrior")


if __name__ == "__main__":
    process_day()