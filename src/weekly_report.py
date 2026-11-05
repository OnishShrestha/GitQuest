
import json
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = ROOT / "data" / "game.json"
REPORT_DIR = ROOT / "reports" / "weekly"


def load_game():
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def generate_weekly_report():
    game = load_game()

    today = date.today()

    # Most recently completed Monday-Sunday week
    this_monday = today - timedelta(days=today.weekday())
    week_end = this_monday - timedelta(days=1)
    week_start = week_end - timedelta(days=6)

    history = game.get("history", [])

    weekly_history = [
        entry for entry in history
        if week_start <= date.fromisoformat(entry["date"]) <= week_end
    ]

    active_days = sum(
        1 for entry in weekly_history
        if entry.get("status") == "active"
    )

    rest_days = sum(
        1 for entry in weekly_history
        if entry.get("status") == "rest"
    )

    weekly_xp = sum(entry.get("xp", 0) for entry in weekly_history)
    weekly_gold = sum(entry.get("gold", 0) for entry in weekly_history)
    weekly_damage = sum(
        entry.get("boss_damage", 0) for entry in weekly_history
    )

    player = game.get("player", {})
    boss = game.get("boss", {})

    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    report_file = REPORT_DIR / f"week-{week_start}-to-{week_end}.md"

    lines = [
        f"# GitQuest Weekly Report",
        "",
        f"**Week:** {week_start} to {week_end}",
        "",
        "## Player Overview",
        "",
        f"- **Player:** {player.get('name', 'Unknown')}",
        f"- **Class:** {player.get('class', 'Unknown')}",
        f"- **Level:** {player.get('level', 1)}",
        f"- **Total XP:** {player.get('xp', 0)}",
        f"- **Gold:** {player.get('gold', 0)}",
        "",
        "## Weekly Activity",
        "",
        f"- **Active days:** {active_days}",
        f"- **Rest days:** {rest_days}",
        f"- **XP earned:** {weekly_xp}",
        f"- **Gold earned:** {weekly_gold}",
        f"- **Boss damage dealt:** {weekly_damage}",
        "",
        "## Weekly Boss",
        "",
        f"- **Boss:** {boss.get('name', 'No boss recorded')}",
        f"- **Health:** {boss.get('hp', 0)}/{boss.get('max_hp', 0)}",
        f"- **Defeated:** {'Yes' if boss.get('defeated') else 'No'}",
        "",
        "## Adventure History",
        ""
    ]

    if weekly_history:
        for entry in weekly_history:
            lines.append(
                f"- **{entry['date']}** — "
                f"{entry.get('event', 'Adventure')} "
                f"({entry.get('status', 'unknown')})"
            )
    else:
        lines.append("No adventures recorded for this week.")

    lines.extend([
        "",
        "---",
        "*Generated automatically by GitQuest.*"
    ])

    report_file.write_text("\n".join(lines), encoding="utf-8")

    print(f"Weekly report generated: {report_file}")


if __name__ == "__main__":
    generate_weekly_report()
