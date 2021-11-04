from random import randint, choice


def flip():
    result_random = choice([True, False])
    answer_on_flip = ""
    answer_on_flip += "Peшка" if result_random else "Орел"

    return answer_on_flip


def roll():
    answer_on_roll = ""
    answer_on_roll += f"Тебе сегодня прилетает {randint(1,100)}"

    return answer_on_roll


def activate_module(func) -> str:
    """Входная точка модуля"""
    active_func = settings["func"].get(func)["entry_point"]

    answer_module = None
    if active_func:
        answer_module = active_func()

    return answer_module


settings = {
    "name": "Flip and roll game",
    "version": "1.0.0",
    "author": "Narteno",
    "date_created": "12.11.2019",
    "entry_point": activate_module,
    "func": {
        "roll": {"name": "roll", "description": "", "entry_point": roll},
        "flip": {"name": "flip", "description": "", "entry_point": flip},
    },
    "templates": {"flip": [r"флип"], "roll": [r"ролл"]},
}
