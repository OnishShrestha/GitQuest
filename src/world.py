AREAS = [
    {
        "level": 1,
        "name": "🌲 Code Forest",
        "enemy": "🐛 Bug Goblin"
    },
    {
        "level": 5,
        "name": "📚 Library of Docs",
        "enemy": "👻 Documentation Ghost"
    },
    {
        "level": 10,
        "name": "🧪 Testing Caverns",
        "enemy": "🧟 Test Zombie"
    },
    {
        "level": 15,
        "name": "⚙️ Automation Factory",
        "enemy": "🤖 Automation Bot"
    },
    {
        "level": 20,
        "name": "🐉 Dragon's Lair",
        "enemy": "🐉 Ancient Dragon"
    }
]


def get_unlocked_areas(level):
    return [
        area
        for area in AREAS
        if level >= area["level"]
    ]