import json
import random
from datetime import date
from pathlib import Path

from achievements import check_achievements
from events import random_event
from inventory import add_item, random_item


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
        return (
            f"🎉 Level Up! "
            f"You reached Level {player['level']}!"
        )

    return None


def damage_boss(game, damage):
    boss = game["boss"]

    if boss["defeated"]:
        return False

    boss["hp"] = max(0, boss["hp"] - damage)

    game["stats"]["boss_damage"] += damage

    if boss["hp"] == 0:
        boss["defeated"] = True
        return True

    return False


def process_day():
    game = load_game()
    player = game["player"]

    today = str(date.today())

    # Prevent the workflow from processing the same day twice.
    if any(
        entry.get("date") == today
        for entry in game.get("history", [])
    ):
        print("Today's adventure has already been processed.")
        return

    # 75% chance of an active day.
    # 25% chance of a rest day.
    active = random.random() < 0.75

    # ---------------------------------------------------------
    # REST DAY
    # ---------------------------------------------------------

    if not active:

        player["days_skipped"] += 1

        # Reset streak for now.
        # We can add streak protection later.
        player["streak"] = 0

        game["history"].append({
            "date": today,
            "status": "rest",
            "event": "🌙 Rest Day",
            "description": "The kingdom rests today."
        })

        save_game(game)

        print()
        print("🌙 REST DAY")
        print()
        print("The kingdom rests today.")
        print("No quest was assigned.")
        print()

        return

    # ---------------------------------------------------------
    # ACTIVE DAY
    # ---------------------------------------------------------

    event = random_event()

    player["days_active"] += 1
    player["streak"] += 1
    player["quests_completed"] += 1

    # XP
    level_message = add_xp(
        game,
        event["xp"]
    )

    # Gold
    player["gold"] += event["gold"]

    # ---------------------------------------------------------
    # ATTRIBUTES
    # ---------------------------------------------------------

    attribute = event.get("attribute")

    if attribute:

        if attribute not in game["attributes"]:
            game["attributes"][attribute] = 0

        game["attributes"][attribute] += 1

    # ---------------------------------------------------------
    # EVENT STATISTICS
    # ---------------------------------------------------------

    event_type = event.get("type")

    if event_type == "bug":
        game["stats"]["bugs_defeated"] += 1

    elif event_type == "docs":
        game["stats"]["docs_improved"] += 1

    elif event_type == "testing":
        game["stats"]["tests_added"] += 1

    elif event_type == "treasure":
        game["stats"]["treasures_found"] += 1

    # ---------------------------------------------------------
    # BOSS DAMAGE
    # ---------------------------------------------------------

    boss_damage = max(
        10,
        event["xp"] // 2
    )

    boss_defeated = damage_boss(
        game,
        boss_damage
    )

    # ---------------------------------------------------------
    # RANDOM TREASURE
    # ---------------------------------------------------------

    treasure_found = False

    if random.random() < 0.20:

        item = random_item()

        add_item(
            game,
            item
        )

        treasure_found = True

    # ---------------------------------------------------------
    # ACHIEVEMENTS
    # ---------------------------------------------------------

    new_achievements = check_achievements(game)

    # ---------------------------------------------------------
    # SAVE HISTORY
    # ---------------------------------------------------------

    history_entry = {
        "date": today,
        "status": "active",
        "event": event["name"],
        "type": event_type,
        "description": event["description"],
        "xp": event["xp"],
        "gold": event["gold"],
        "boss_damage": boss_damage
    }

    if attribute:
        history_entry["attribute"] = attribute

    if treasure_found:
        history_entry["treasure"] = item["name"]

    if boss_defeated:
        history_entry["boss_defeated"] = True

    if new_achievements:
        history_entry["achievements"] = new_achievements

    game["history"].append(
        history_entry
    )

    save_game(game)

    # ---------------------------------------------------------
    # DISPLAY RESULTS
    # ---------------------------------------------------------

    print()
    print("╔════════════════════════════════════╗")
    print("║        ⚔️ GITQUEST ADVENTURE       ║")
    print("╚════════════════════════════════════╝")
    print()

    print(event["name"])
    print(event["description"])
    print()

    print(f"⭐ +{event['xp']} XP")
    print(f"💰 +{event['gold']} Gold")
    print(f"🐉 -{boss_damage} Boss HP")

    if attribute:
        print(
            f"📊 +1 {attribute.capitalize()}"
        )

    if treasure_found:
        print()
        print(
            f"🎁 Treasure found: "
            f"{item['name']} "
            f"({item['rarity']})"
        )

    if level_message:
        print()
        print(level_message)

    if new_achievements:
        print()
        print("🏆 ACHIEVEMENT UNLOCKED!")

        for achievement in new_achievements:
            print(f"   🏆 {achievement}")

    if boss_defeated:
        print()
        print("╔════════════════════════════════════╗")
        print("║       💀 BOSS DEFEATED! 💀         ║")
        print("╚════════════════════════════════════╝")
        print()
        print(
            f"You defeated {game['boss']['name']}!"
        )

    print()
    print(f"Level: {player['level']}")
    print(f"XP: {player['xp']}")
    print(f"Gold: {player['gold']}")
    print(f"Streak: {player['streak']}")
    print()


if __name__ == "__main__":
    process_day()