def flip():
    from random import choice

    result_random = choice([True, False])
    answer_on_flip = ""
    answer_on_flip += "Peшка" if result_random else "Орел"

    return answer_on_flip

def roll():
    from random import randint

    answer_on_roll = ""
    answer_on_roll += f"Тебе сегодня прилетает {randint(1,100)}"

    return answer_on_roll

def activate_module(func, *args, **kwargs):
    """
    Входная точка модуля.
    """
    active_func = settings["func"].get(func)[0]

    answer_module = ""
    if active_func:
        answer_module = active_func()

    return answer_module

def getSettings():
    """
    Возвращает настройки модуля в виде словаря.
    ```

    ==> {
        "name"          : "Flip and roll game",
        "version"       : "1.0.0",
        "author"        : "Narteno",
        "date_created"  : "12.11.2019",
        "entry_point"   : activate_module,
        "func"          : {
            "roll" : (roll, "Описание"),
            "flip" : (flip, "Описание")      
        },
        "templates"     : {
            "flip" : [
                r"флип"
            ],
            "roll" : [
                r"ролл"
            ]
        }
    ```
    """
    return settings

settings = {
    "name"          : "Flip and roll game",
    "version"       : "1.0.0",
    "author"        : "Narteno",
    "date_created"  : "12.11.2019",
    "entry_point"   : activate_module,
    "func"          : {
        "roll" : (roll, ""),
        "flip" : (flip, "")
    },
    "templates"     : {
        "flip" : [
            r"флип"
        ],
        "roll" : [
            r"ролл"
        ]
    }
}