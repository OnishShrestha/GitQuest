ITEMS = [
    {
        "name": "🧪 XP Potion",
        "rarity": "Common",
        "value": 100
    },
    {
        "name": "💎 Git Crystal",
        "rarity": "Rare",
        "value": 250
    },
    {
        "name": "🐉 Dragon Scale",
        "rarity": "Epic",
        "value": 500
    },
    {
        "name": "👑 Crown of Commits",
        "rarity": "Legendary",
        "value": 1000
    }
]


def add_item(game, item):
    game["inventory"].append(item)


def random_item():
    import random
    return random.choice(ITEMS)