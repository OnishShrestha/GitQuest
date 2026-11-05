
import json
import random
from datetime import date
from pathlib import Path

from achievements import (
    check_achievements,
    record_boss_defeat,
    roll_hidden_achievement
)
from events import random_event
from inventory import add_item, random_item


ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = ROOT / "data" / "game.json"


def load_game():
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def save_game(game):
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(
            game,
            file,
            indent=2,
            ensure_ascii=False
        )


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
    boss = game.get("boss")

    if not boss:
        return False, 0

    if boss.get("defeated") or boss.get("hp", 0) <= 0:
        return False, 0

    # Only count the damage actually needed to defeat the boss.
    actual_damage = min(damage, boss["hp"])

    boss["hp"] = max(0, boss["hp"] - actual_damage)

    game.setdefault("stats", {})
    game["stats"]["boss_damage"] = (
        game["stats"].get("boss_damage", 0) + actual_damage
    )

    if boss["hp"] <= 0:
        boss["hp"] = 0
        boss["defeated"] = True
        return True, actual_damage

    return False, actual_damage


def normalize_achievement_result(result):
    """
    Convert achievement results into a list of displayable names.
    Supports a single name or a list of names.
    """
    if not result:
        return []

    if isinstance(result, str):
        return [result]

    if isinstance(result, list):
        return [
            item if isinstance(item, str) else item.get("name", str(item))
            for item in result
        ]

    return []


def process_day():
    game = load_game()
    player = game["player"]

    today = date.today().isoformat()

    game.setdefault("history", [])
    game.setdefault("stats", {})
    game.setdefault("achievements", [])

    # Prevent the workflow from processing the same day twice.
    if any(
        entry.get("date") == today
        for entry in game["history"]
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

    # ---------------------------------------------------------
    # XP AND GOLD
    # ---------------------------------------------------------

    level_message = add_xp(game, event["xp"])

    player["gold"] += event["gold"]

    # ---------------------------------------------------------
    # ATTRIBUTES
    # ---------------------------------------------------------

    attribute = event.get("attribute")

    if attribute:
        game.setdefault("attributes", {})

        if attribute not in game["attributes"]:
            game["attributes"][attribute] = 0

        game["attributes"][attribute] += 1

    # ---------------------------------------------------------
    # EVENT STATISTICS
    # ---------------------------------------------------------

    event_type = event.get("type")

    if event_type == "bug":
        game["stats"]["bugs_defeated"] = (
            game["stats"].get("bugs_defeated", 0) + 1
        )

    elif event_type == "docs":
        game["stats"]["docs_improved"] = (
            game["stats"].get("docs_improved", 0) + 1
        )

    elif event_type == "testing":
        game["stats"]["tests_added"] = (
            game["stats"].get("tests_added", 0) + 1
        )

    elif event_type == "treasure":
        game["stats"]["treasures_found"] = (
            game["stats"].get("treasures_found", 0) + 1
        )

    # ---------------------------------------------------------
    # BOSS DAMAGE
    # ---------------------------------------------------------

    boss_damage = max(10, event["xp"] // 2)

    boss_defeated, actual_boss_damage = damage_boss(
        game,
        boss_damage
    )

    # ---------------------------------------------------------
    # BOSS DEFEAT RECORD
    # ---------------------------------------------------------

    boss_achievements = []

    if boss_defeated:
        # Record the boss name, generation, week, and defeat date.
        result = record_boss_defeat(game)

        boss_achievements.extend(
            normalize_achievement_result(result)
        )

    # ---------------------------------------------------------
    # RANDOM TREASURE
    # ---------------------------------------------------------

    treasure_found = False
    item = None

    if random.random() < 0.20:
        item = random_item()

        add_item(game, item)

        treasure_found = True

    # ---------------------------------------------------------
    # NORMAL ACHIEVEMENTS
    # ---------------------------------------------------------

    new_achievements = check_achievements(game)

    new_achievements = normalize_achievement_result(
        new_achievements
    )

    # Include achievements unlocked by defeating the boss.
    for achievement in boss_achievements:
        if achievement not in new_achievements:
            new_achievements.append(achievement)

    # ---------------------------------------------------------
    # RARE HIDDEN ACHIEVEMENT
    # ---------------------------------------------------------

    # One hidden-achievement roll per day.
    hidden_result = roll_hidden_achievement(game)

    hidden_achievements = normalize_achievement_result(
        hidden_result
    )

    for achievement in hidden_achievements:
        if achievement not in new_achievements:
            new_achievements.append(achievement)

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
        "boss_damage": actual_boss_damage
    }

    if attribute:
        history_entry["attribute"] = attribute

    if treasure_found:
        history_entry["treasure"] = item["name"]

    if boss_defeated:
        boss = game["boss"]

        history_entry["boss_defeated"] = True
        history_entry["boss_name"] = boss["name"]
        history_entry["boss_generation"] = boss.get(
            "generation", 1
        )

    if new_achievements:
        history_entry["achievements"] = new_achievements

    game["history"].append(history_entry)

    # Save all player, boss, achievement, and history changes.
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
    print(f"🐉 -{actual_boss_damage} Boss HP")

    if attribute:
        print(f"📊 +1 {attribute.capitalize()}")

    if treasure_found:
        print()
        print(
            f"🎁 Treasure found: "
            f"{item['name']} ({item['rarity']})"
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
        boss = game["boss"]

        generation = boss.get("generation", 1)
        generation_label = boss.get(
            "generation_label",
            str(generation)
        )

        print()
        print("╔════════════════════════════════════╗")
        print("║       💀 BOSS DEFEATED! 💀         ║")
        print("╚════════════════════════════════════╝")
        print()

        print(f"You defeated {boss['name']}!")
        print(f"Generation: {generation_label}")
        print(f"Defeated on: {today}")

    print()
    print(f"Level: {player['level']}")
    print(f"XP: {player['xp']}")
    print(f"Gold: {player['gold']}")
    print(f"Streak: {player['streak']}")
    print()


if __name__ == "__main__":
    process_day()
