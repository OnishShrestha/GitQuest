CLASSES = {
    "Warrior": {
        "description": "Specializes in bugs and coding quests.",
        "bonus": "strength"
    },
    "Mage": {
        "description": "Specializes in documentation and knowledge.",
        "bonus": "knowledge"
    },
    "Guardian": {
        "description": "Specializes in testing and reliability.",
        "bonus": "defense"
    },
    "Ranger": {
        "description": "Specializes in automation and speed.",
        "bonus": "speed"
    }
}


def get_class(name):
    return CLASSES.get(name, CLASSES["Warrior"])