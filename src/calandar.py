from datetime import date


def generate_calendar(history, year, month):

    days = {}

    for entry in history:

        try:
            entry_date = date.fromisoformat(entry["date"])
        except (KeyError, ValueError):
            continue

        if (
            entry_date.year == year
            and entry_date.month == month
        ):
            days[entry_date.day] = entry["status"]

    return days


def calendar_symbol(status):

    if status == "active":
        return "🟩"

    if status == "rest":
        return "🌙"

    return "⬜"