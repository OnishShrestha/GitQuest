
import random
from datetime import date


ACHIEVEMENTS = [
    {
        "name": "First Quest",
        "description": "Complete your first quest.",
        "requirement": lambda game:
            game.get("stats", {}).get("quests_completed", 0) >= 1
    },
    {
        "name": "Bug Slayer",
        "description": "Defeat 5 bugs.",
        "requirement": lambda game:
            game.get("stats", {}).get("bugs_defeated", 0) >= 5
    },
    {
        "name": "Scholar",
        "description": "Improve documentation 5 times.",
        "requirement": lambda game:
            game.get("stats", {}).get("docs_improved", 0) >= 5
    },
    {
        "name": "Scientist",
        "description": "Complete 5 testing quests.",
        "requirement": lambda game:
            game.get("stats", {}).get("tests_added", 0) >= 5
    },
    {
        "name": "Century",
        "description": "Complete 100 quests.",
        "requirement": lambda game:
            game.get("stats", {}).get("quests_completed", 0) >= 100
    },
    {
        "name": "Dragon Slayer",
        "description": "Defeat your first weekly boss.",
        "requirement": lambda game:
            len(game.get("boss_history", [])) >= 1
    },
    {
        "name": "Boss Hunter",
        "description": "Defeat 5 weekly bosses.",
        "requirement": lambda game:
            len(game.get("boss_history", [])) >= 5
    },
    {
        "name": "Legendary Warrior",
        "description": "Defeat 10 weekly bosses.",
        "requirement": lambda game:
            len(game.get("boss_history", [])) >= 10
    },
    {
        "name": "Return of the Dragon",
        "description": "Defeat a boss in its 2nd generation.",
        "requirement": lambda game:
            any(b.get("generation", 1) >= 2
                for b in game.get("boss_history", []))
    }
]


# Extremely rare achievements.
HIDDEN_ACHIEVEMENTS = [
    {
        "name": "The Chosen Commit",
        "description": "The kingdom has recognized your extraordinary luck."
    },
    {
        "name": "Phantom Developer",
        "description": "You discovered a secret hidden beyond the code."
    },
    {
        "name": "Beyond the Code",
        "description": "You found something that was never meant to be found."
    },
    {
        "name": "The 1-in-1000",
        "description": "You experienced a legendary moment of luck."
    }
]


def ordinal(number):
    """Convert numbers into 1st, 2nd, 3rd, 4th, etc."""
    if 10 <= number % 100 <= 20:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(
            number % 10, "th"
        )

    return f"{number}{suffix}"


def award_achievement(game, name, description, hidden=False):
    """Save an achievement with its unlock date."""
    today = date.today().isoformat()

    achievements = game.setdefault("achievements", [])

    # Support both the old string format and the new dictionary format.
    existing_names = {
        a if isinstance(a, str) else a.get("name")
        for a in achievements
    }

    if name in existing_names:
        return False

    achievements.append({
        "name": name,
        "description": description,
        "date": today,
        "hidden": hidden
    })

    print(f"\n🏆 ACHIEVEMENT UNLOCKED: {name}")
    print(description)
    print(f"📅 Date: {today}")

    return True


def check_achievements(game):
    """Check and unlock all normal achievements."""
    unlocked = []

    for achievement in ACHIEVEMENTS:
        name = achievement["name"]

        existing_names = {
            a if isinstance(a, str) else a.get("name")
            for a in game.setdefault("achievements", [])
        }

        if name in existing_names:
            continue

        if achievement["requirement"](game):
            if award_achievement(
                game,
                name,
                achievement["description"]
            ):
                unlocked.append(name)

    return unlocked


def record_boss_defeat(game):
    """Record a defeated boss, its generation and defeat date."""
    boss = game.get("boss")

    if not boss or boss.get("defeated"):
        return False

    if boss.get("hp", 0) > 0:
        return False

    boss["hp"] = 0
    boss["defeated"] = True

    generation = boss.get("generation", 1)

    record = {
        "name": boss.get("name", "Unknown Boss"),
        "generation": generation,
        "generation_label": ordinal(generation),
        "week": game.get("boss_week"),
        "defeated_on": date.today().isoformat()
    }

    game.setdefault("boss_history", []).append(record)

    print(
        f"💀 {record['name']} "
        f"({record['generation_label']} Generation) defeated!"
    )

    check_achievements(game)

    return True


def roll_hidden_achievement(game):
    """One 1-in-1000 hidden achievement chance per calendar day."""
    today = date.today().isoformat()

    checked_dates = game.setdefault(
        "hidden_achievement_checks", []
    )

    if today in checked_dates:
        return None

    checked_dates.append(today)

    if random.randint(1, 1000) != 1:
        return None

    existing_names = {
        a if isinstance(a, str) else a.get("name")
        for a in game.setdefault("achievements", [])
    }

    available = [
        a for a in HIDDEN_ACHIEVEMENTS
        if a["name"] not in existing_names
    ]

    if not available:
        return None

    secret = random.choice(available)

    if award_achievement(
        game,
        secret["name"],
        secret["description"],
        hidden=True
    ):
        return secret["name"]

    return None
