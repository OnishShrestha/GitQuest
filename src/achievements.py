ACHIEVEMENTS = [
    {
        "name": "First Quest",
        "description": "Complete your first quest.",
        "requirement": lambda game:
            game["stats"]["quests_completed"] >= 1
    },
    {
        "name": "Bug Slayer",
        "description": "Defeat 5 bugs.",
        "requirement": lambda game:
            game["stats"]["bugs_defeated"] >= 5
    },
    {
        "name": "Scholar",
        "description": "Improve documentation 5 times.",
        "requirement": lambda game:
            game["stats"]["docs_improved"] >= 5
    },
    {
        "name": "Scientist",
        "description": "Complete 5 testing quests.",
        "requirement": lambda game:
            game["stats"]["tests_added"] >= 5
    },
    {
        "name": "Century",
        "description": "Complete 100 quests.",
        "requirement": lambda game:
            game["stats"]["quests_completed"] >= 100
    }
]


def check_achievements(game):
    unlocked = []

    for achievement in ACHIEVEMENTS:

        name = achievement["name"]

        if name in game["achievements"]:
            continue

        if achievement["requirement"](game):
            game["achievements"].append(name)
            unlocked.append(name)

    return unlocked