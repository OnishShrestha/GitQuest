import random


EVENTS = [
    {
        "name": "🎁 Treasure Found",
        "description": "You discovered a hidden Git Crystal.",
        "xp": 50,
        "gold": 100,
        "attribute": "knowledge"
    },
    {
        "name": "🐛 Bug Ambush",
        "description": "A Bug Goblin attacked the kingdom!",
        "xp": 100,
        "gold": 50,
        "attribute": "strength"
    },
    {
        "name": "📚 Ancient Knowledge",
        "description": "You discovered forgotten documentation.",
        "xp": 75,
        "gold": 75,
        "attribute": "knowledge"
    },
    {
        "name": "🧪 Testing Challenge",
        "description": "A Test Zombie appeared in the testing caverns.",
        "xp": 100,
        "gold": 60,
        "attribute": "defense"
    },
    {
        "name": "⚡ Speed Trial",
        "description": "The kingdom challenges your automation skills.",
        "xp": 125,
        "gold": 80,
        "attribute": "speed"
    }
]


def random_event():
    return random.choice(EVENTS)