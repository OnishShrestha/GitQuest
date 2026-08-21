import random


BOSSES = [
    {
        "name": "🐉 README Dragon",
        "hp": 500
    },
    {
        "name": "🧟 Test Zombie",
        "hp": 750
    },
    {
        "name": "👹 Dependency Demon",
        "hp": 1000
    },
    {
        "name": "🐍 Bug Serpent",
        "hp": 1250
    },
    {
        "name": "🤖 Automation Overlord",
        "hp": 2000
    }
]


def random_boss():
    boss = random.choice(BOSSES)

    return {
        "name": boss["name"],
        "max_hp": boss["hp"],
        "hp": boss["hp"],
        "defeated": False
    }