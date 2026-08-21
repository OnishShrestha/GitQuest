import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = ROOT / "data" / "game.json"
README_FILE = ROOT / "README.md"


def load_game():
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def progress_bar(current, maximum, size=10):
    if maximum <= 0:
        return "░" * size

    filled = int((current / maximum) * size)
    filled = min(filled, size)

    return "█" * filled + "░" * (size - filled)


def generate_dashboard(game):
    player = game["player"]
    stats = game["stats"]
    boss = game["boss"]

    xp_current = player["xp"] % 100
    xp_bar = progress_bar(xp_current, 100)

    boss_bar = progress_bar(
        boss["hp"],
        boss["max_hp"],
        10
    )

    achievements = game["achievements"]

    achievement_text = (
        "\n".join(f"- 🏆 {a}" for a in achievements)
        if achievements
        else "- No achievements yet."
    )

    recent = game["history"][-5:]

    history_text = []

    for entry in reversed(recent):
        if entry["status"] == "rest":
            history_text.append(
                f"- {entry['date']} — 🌙 Rest Day"
            )
        else:
            history_text.append(
                f"- {entry['date']} — {entry['event']} "
                f"(+{entry['xp']} XP)"
            )

    return f"""# ⚔️ GitQuest

### 🧙 Onish — Level {player["level"]}

**XP:** `{player["xp"]}`

`{xp_bar}`

**💰 Gold:** {player["gold"]}

**🔥 Current Streak:** {player["streak"]} days

---

## 🗺️ Kingdom Statistics

| Statistic | Value |
|---|---:|
| ⚔️ Quests Completed | {player["quests_completed"]} |
| 📅 Active Days | {player["days_active"]} |
| 🌙 Rest Days | {player["days_skipped"]} |
| 🐛 Bugs Defeated | {stats["bugs_defeated"]} |
| 📚 Docs Improved | {stats["docs_improved"]} |
| 🧪 Tests Added | {stats["tests_added"]} |
| 🎁 Treasures Found | {stats["treasures_found"]} |

---

## 🐉 Weekly Boss

### {boss["name"]}

HP: `{boss["hp"]}/{boss["max_hp"]}`

`{boss_bar}`

Status:

**{"💀 DEFEATED" if boss["defeated"] else "🔥 Still Alive" }**

---

## 🏆 Achievements

{achievement_text}

---

## 📜 Recent Adventures

{chr(10).join(history_text)}

---

## 🎮 How It Works

GitQuest is an autonomous developer RPG powered by Python and GitHub Actions.

Every day the kingdom decides whether to:

- ⚔️ Assign a quest
- 🎁 Discover treasure
- 🐛 Fight a bug
- 📚 Improve documentation
- 🧪 Strengthen testing
- 🌙 Take a rest day

The game automatically updates itself through GitHub Actions.

---

*The kingdom never sleeps... except on rest days.* 🌙
"""


if __name__ == "__main__":
    game = load_game()
    dashboard = generate_dashboard(game)

    with open(README_FILE, "w", encoding="utf-8") as file:
        file.write(dashboard)

    print("README dashboard updated.")