"""
Файл с настройками бота, регулировка данного файла позволяет создать своего уникального бота.
"""

class CONST:
    """
    Класс хрянящий все неизменяющиеся переменные const.
    """

    token           = r""           # Токен хранится в виде строки

    bot_group_id    = 123456789     # id группы бота хранится в виде числа. Пример: 123456789

    def_templ       = r""           # шаблон слова на который бот должен всегда давать какой-либо ответ, лучше всего сюда поставить имя бота

    join_templ      = r"\s.*?"      # шаблон слова или пробела, с помощью которого будет происходить соединение с другими шаблонами

    admin_id        = 123456789     # id администартора бота
    
    def_time_work   = "ALL"         # значение времени работы бота, которое устанавливатся по умолчанию для всех групп (Не указанных в time_work_group)

    all_templ  = {                  # набор всех шаблонов сгрупированных в наборы однородных слов с.м. пример
        "приветствие"  : {
            "здравствуй"    : r"здр.вств.й",
            "привет"        : r"пр.в.т",
        },
        "прощание"   : {
            "пока"          : r"п.к.",
            "до свидания"   : r"д.\sсв.д.н.я"
        }
    }

    answers    =  {                 # набор всех шаблонов ответов на конкретные слова, разбитые по редкости выпадения
        'по умолчанию' : {
            "common" : [
            ],

            "uncommon" : [
            ],

            "rare" : [
            ],

            "legendary" : [
            ],
        },

        'приветствие' : {

            "здравствуй": {
                "common" : [
                    "Здравствуйте, чем могу помочь?",
                    "Здравствуй друг, чем я мог бы тебе помочь?",
                ],
            },

            "привет" : {
                "common" : [
                    "Привет, чем могу помочь?",
                    "Привет друг, чем я мог бы тебе помочь?",
                ],
            },    
        },

        'прощание' : {
            
            "пока"          : {
                "common" : [
                    "Пока, буду тебя ждать.",
                ],
            },

            "до свидания"   : {
                "common" : [
                    "До свидания, надеюсь я тебе помог.",
                ],
            }
        },
    }

    type_time_work = [              # Все варианты времени работы бота
        "ALL",
        "NIGHT_MSK",
        "DAY_MSK",
        "CUSTOM",
    ]

    time_work_group = {             # Время работы конкретной группы (0 - это 00:00, а 8 - это 08:00, from 0 to 8, значит с 00:00 до 08:00 по МСК)
            123456789 : {
                "type"  : type_time_work[0],
            },

            123456789 : {
                "type"  : type_time_work[1],
                "from"  : 0,
                "to"    : 8,
            },
    }

    command  = {                    # Список команд доступных боту из коробки, для того, 
                                    # чтобы расширить этот список необходимо вносить правки в файл components/command.py.
                                    # Публичные команды доступны всем пользователям, приватные только администатору.
        "public" : {
            "выключить бота"        : {
                "templates" : [
                    "выкл*\sбот*",
                    "бот\sвыкл*",
                ],
            },

            "включить бота"         : {
                "templates" : [
                    "вкл*\sбот*",
                    "бот\sвкл*",
                ],
            },

            "показать стат группы"  : {
                "templates" : [
                    "п.к.жи\sстат",
                ],
            },
        },

        "private" : {
            "показать всю стат"     : {
                "templates" : [
                    "п.к.жи\sвсю\sстат",
                ],
            },
        },
    }

    list_all_com = [                # Список всех команд, усли не внести команду в этот список, она работать не будет
        "включить бота",
        "выключить бота",
        "показать стат группы",
        "показать всю стат",
    ]

    prohabilities   = {             # Шанс выпадения ответа бота для каждого из типов редкости
        "common" : 0.5,
        "uncommon" : 0.25, 
        "rare" : 0.05, 
        "legendary" : 0.005,
    }

templ_and_respons = {               # Список хранящий все отношения между словами из шаблона и ответами. 
                                    # При внесении новых слов и ответов на них необходимо так же в данном списке предоставить зависимости
        CONST.def_templ                                 : CONST.answers['по умолчанию'],
        CONST.all_templ["приветствие"]['здравствуй']    : CONST.answers["приветствие"]['здравствуй'],
        CONST.all_templ["приветствие"]['здравствуй']    : CONST.answers["приветствие"]['здравствуй'],
        CONST.all_templ["прощание"]["пока"]             : CONST.answers['прощание']["пока"],
        CONST.all_templ["прощание"]["до свидания"]      : CONST.answers['прощание']["до свидания"],
    }