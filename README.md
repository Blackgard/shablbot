<p align="center">
 <img src="./images/shablbot.png" alt="logo shablbot">
</p>
<div align="center">

[![Build](https://img.shields.io/azure-devops/build/sasna142/026fd26f-bb59-48fd-bb91-6d9ebe113f87/2)]() [![License](https://img.shields.io/github/license/blackgard/shablbot)]()

</div>

---------------------------------

🤖 Бот написанный на Python для социальной сети Вконтакте, работающий через VkBotLongPull.

## 💭 О проекте <a name="#about"></a>

Данный проект разрабатывался с целью облегчить создание ботов для людей, которые мало/плохо знакомы с программированием. Бот устроен таким образом, что Вам нужно написать минимальное количество кода, чтобы добавить новый функционал. В последствии бот будет дорабатываться и развиваться.

## 🎈 Установка <a name="#install"></a>

Требуется **Python 3.9+**.

Можете воспользоваться командой [pip](https://pypi.org/project/pip/):
```cmd
 pip install shablbot
```
Или же использовать [poetry](https://python-poetry.org/):
```poetry
 poetry add shablbot
```

## :dizzy: Инициализация <a name="init"></a>

Чтобы начать работу с ботом необходимо выполнить инициализацию компонентов бота:

Для этого нужно выполнить команду:

windows
```cmd
 C:\shablbot> py -m shablbot --init
```

linux
```bash
 blackgard@bar:~/shablbot$ python3 -m shablbot --init
```

После чего в папке, откуда был вызван скрипт, будут созданы каталоги с следующей структурой:
```
📦*yourfolder*
 ┣ 📂commands
 ┃  ┣ 📂private
 ┃  ┃  ┗ 🐍 show_id_active_chats.py
 ┃  ┣ 📂public
 ┃  ┃  ┣ 🐍 chat_bot_off.py
 ┃  ┃  ┣ 🐍 chat_bot_on.py
 ┃  ┃  ┗ 🐍 chat_show_statistics.py
 ┣ 📂keyboards
 ┃  ┣ 📜 clear.json
 ┃  ┗ 📜 default.json
 ┣ 📂modules
 ┃  ┣ 📂ai
 ┃  ┃  ┗ 🐍 neural_chat.py
 ┃  ┗ 📂games
 ┃     ┗ 🐍 flip_and_roll.py
 ┣ 📂phrases
 ┃  ┣ 📜 _default.json
 ┃  ┣ 📜 bye.json
 ┃  ┗ 📜 hello.json
 ┣ 📂settings
 ┃  ┗ 🐍 settings.py
 ┣ 📂data
 ┃  ┗ 📜 chat_settings.json
 ┗ 🐍 manager.py
```
<div align="center"><font size="2" style="text-align:center">Более подробно про каждый из каталогов будет рассказано далее</font></div>
<br>

После этого можно перейти к настройке бота.

## ⏳ Стартовая настройка <a name="start_setting"></a>
Настройка бота производится с помощью редактирования файла <b>[settings.py](#init)</b>, находящегося в папке settings, созданной на шаге выше.

Обязательные поля для работы бота:
1. **TOKEN** - ключ доступа к сообществу вконтакте, ключ должен быть с правами к сообщениям сообщества. [Как получить токен для бота?](#how_get_bot_token)
```python
  TOKEN = os.getenv("TOKEN") # "1234566789908798689764867293876243987" (str)
```
2. **BOT_CHAT_ID** - id страницы вконтакте сообщества, от лица которого будет работать бот.
```python
  BOT_CHAT_ID = os.getenv("BOT_CHAT_ID") # 123456789 (int)
```
3. **DEFAULT_REACTION_TEMPLATES** - слова на которые бот будет всегда как-либо реагировать.
```python
  DEFAULT_REACTION_TEMPLATES = (r"бот",) # (tuple)
```
4. **ADMIN_ID** - id страницы вконтакте человека, от лица которого будет происходить администрирование бота.
```python
  ADMIN_ID = os.getenv("ADMIN_ID") # 123456789 (int)
```
Остальные параметры для начального запуска бота менять не нужно.

🔔 *Советую для хранения токена и id-ов использовать .env файл. К примеру используйте [python-dotenv](https://pypi.org/project/python-dotenv/).*

## 🚀 Запуск бота

Для запуска бота мы используем файл [manager.py](#init), созданный на первом шаге.

windows
```cmd
  C:\shablbot> py manager.py --run
```

linux
```bash
  blackgard@bar:~/shablbot$ python3 manager.py --run
```

Если вы все правильно сделали, то в консоли увидите следующее сообщение:
```console
  2099-99-99 at -1:99:99 | INFO | ------- Бот запущен / Bot is runing -------
```

## :card_file_box: Модульность бота <a name="bot_modules"></a>
1. [Модуль команды](#bot_modules_commands)
2. [Модуль клавиатуры](#bot_modules_keyboards)
3. [Модуль пользовательских модулей](#bot_modules_modules)
4. [Модуль фраз](#bot_modules_phrases)
5. [Модуль настроек](#bot_modules_settings)


То, как бот обрабатывает команды и сообщения от Вас спрятано. По этому Вам доступны 5 типов модулей, для расширения и настройки бота:

### commands <a name="bot_modules_commands"></a>
Модуль отвечающий за команды управления ботом. Нужен для администрирования. Делятся на два типа:
1. <b>private</b> - доступные и выполняемые только администратору бота (`ADMIN_ID`)
2. <b>public</b> - доступные всем пользователям

> :bell: Команды нужно подключать в настройках бота. Переменная <b>ACTIVE_COMMANDS</b>.

Для добавления новой команды вам нужно создай файл в папке private/public с \*название_команды\*.py.

В созданном файле нужно создать переменную command_settings с следующей структурой:

```py
command_settings = {
    # Код команды. Должен быть уникальным.
    "code": "bot_off",
    # Название команды. Публичная переменная.
    "name": "Выключить бота",
    # Слова, на которые бот будет реагировать.
    # Может быть регулярным выражением.
    "templates": ["выкл бот", "бот выкл"],
    # Ответ бота, на результат выполненной команды.
    "answer": "Теперь бот не читает сообщения в чате",
    # Описание команды. Публичная переменная.
    "description": "Команда для выключения бота в чате (Внутри чата)",
    # Метод обработки templates. Если normal, то сравнивает как слова.
    # Если regular, то сравнивает как регулярные выражения.
    "method": "normal",
    # Какие переменные нужны для выполнения команды.
    # Доступные значения = processed_chat, chats, commands;
    "need": ["processed_chat",],
    # Входная точка для выполнения команды.
    # Может быть любой функцией.
    "entry_point": command
}
```

Функция выключения бота в чате:

```py
def command(processed_chat: Chat) -> None:
    processed_chat.turn_off()
```

### keyboards <a name="bot_modules_keyboards"></a>
Модуль отвечающий за варианты клавиатуры бота. Нужен для настройки сообщений, если вы хотите использовать клавиатуру в сообщениях бота.

[Про клавиатуру Vk подробнее читать тут](https://vk.com/dev/bots_docs_3)

> :bell: Клавиатуры нужно подключать в настройках бота. Переменная <b>KEYBOARDS</b>.

> :warning: *Обязательно для работы бота нужны, "clear.json" и "default.json"*

### modules <a name="bot_modules_modules"></a>
Модуль отвечающий за пользовательские модули для бота. К таким модулям можно отнести:
- Игры
- Утилиты (Погода, время, конвертирование валюты)

> :bell: Модули нужно подключать в настройках бота. Переменная <b>ACTIVE_MODULES</b>.

> :warning: *Данный блок еще не совершенен, т.к. всегда требует возврата строки как ответа, в будущем будет как ответ отправлять все типы данных*

Для создания модуля Вам необходимо создать файл с названием модуля и добавить туда переменную settings с следующей структурой:

```py
settings = {
    # Название модуля.
    "name": "Flip and roll game",
    # Версия модуля.
    "version": "1.0.0",
    # Автор модуля.
    "author": "Narteno",
    # Дата создания модуля.
    "date_created": "12.11.2019",
    # Входная точка обработки модуля.
    "entry_point": activate_module,
    # Обрабатывающие запросы функции модуля.
    # В себя включают название функции, описание
    # и входную точку. Нужен для более гибкой настройки.
    "func": {
        "roll": {"name": "roll", "description": "", "entry_point": roll},
        "flip": {"name": "flip", "description": "", "entry_point": flip},
    },
    # Фразы для реакции. Разделяются по функциям модуля.
    "templates": {"flip": [r"флип"], "roll": [r"ролл"]},
}
```

Входная точка модуля должна иметь такую структуру, но не ограничена этим:

```py
def activate_module(func) -> str:
    """Входная точка модуля"""
    active_func = settings["func"].get(func)["entry_point"]

    # Если переменная ответа будет в значении None.
    # То бот не отправит сообщение пользователю.
    answer_module = None
    if active_func:
        answer_module = active_func()

    return answer_module
```

[Подробнее о структуре кастомных модулей смотрите тут flip_and_roll.py](/shablbot/init/modules/games/flip_and_roll.py)

#### Нейросети (OpenRouter и Polza.ai)

Бот поддерживает [OpenRouter](https://openrouter.ai/) и [Polza.ai](https://polza.ai/). Провайдер и модель настраиваются через `.env`.

##### Режим `standalone` (рекомендуется)

Бот отвечает через нейросеть **без префиксов** `ии` / `ai` / `gpt`. Понимает обычные фразы: «привет», «выключи бота», «помоги».

```env
AI_ENABLED=true
AI_MODE=standalone
AI_PROVIDER=openrouter
AI_MODEL=openai/gpt-4o-mini
OPENROUTER_API_KEY=your_key
```

В беседах бот реагирует, когда к нему обращаются (шаблоны из `DEFAULT_REACTION_TEMPLATES`). В личных сообщениях — на любое сообщение.

Нейросеть сама распознаёт команды (`bot_off`, `bot_on`, `help`) и выполняет их.

##### Режим `module` (с префиксом)

```env
AI_ENABLED=true
AI_MODE=module
AI_PROVIDER=polza
AI_MODEL=openai/gpt-4o
POLZA_API_KEY=your_key
```

Добавьте в `ACTIVE_MODULES`: `"ai.neural_chat"`. Команда в чате: `ии Привет!`

##### Дополнительные переменные

| Переменная | Описание | По умолчанию |
|------------|----------|--------------|
| `AI_SYSTEM_PROMPT` | Системный промпт | краткий ассистент VK-бота |
| `AI_MAX_TOKENS` | Лимит токенов ответа | `1024` |
| `AI_TEMPERATURE` | Креативность | `0.7` |
| `AI_HISTORY_LIMIT` | Сообщений в истории | `10` |
| `AI_TIMEOUT` | Таймаут запроса (сек) | `60` |

История диалога хранится в памяти бота (до `AI_HISTORY_LIMIT` сообщений на пользователя).

### phrases <a name="bot_modules_phrases"></a>
Модуль отвечающий за фразы, на которые бот реагирует. Содержит в себе файлы <b>.json</b> формата.

> :bell: Все фразы из папки подгружаются автоматически. Вы можете исключить ненужные фразы используя в настройках переменную <b>EXCLUDED_PHRASES</b>.

json файл должен содержать следующую структуру:

> :warning: *Значения с пометкой "_comment" в реальном файле не должны пристутствовать.*

```json
{
    "#group_comment#":"Стандартная группа. нельзя удалять"
    "group": "default",

    "#words_comment#":"Список слов входящих в группу"
    "words": {
        "#main_comment#":"Название слова, на которое бот реагирует. Может содержать любые символы. Для файла _default.json 'main' обязательное системное значение"
        "main": {
            "#templates_comment#":"Фразы для реакции"
            "templates": [ "бот" ],
            "#answer_comment#":"Варианты ответа разбитые по редкости"
            "answer": {
                "common": ["Я бот"],
                "uncommon": ["Я почти бот"],
                "rare": ["Я точно бот"],
                "legendary": ["А может быть это ты бот?"]
            },
            "#templates_comment#":"Ключ клавиатуры, которую нужно отправить для данного слова."
            "keyboard": "default"
        },
    }
}
```

### settings <a name="bot_modules_settings"></a>
Модуль отвечающий за настройки бота. Все настройки производятся в файле settings.py. В файле для каждой переменной имеются комментарии, поясняющие, что в них хранится.

Pydantic-модели настроек (`SettingsModel` и связанные типы) поставляются вместе с пакетом `shablbot` и импортируются из `shablbot.settings` — отдельный `settings_model.py` в проекте больше не нужен:

```python
from shablbot.settings import SettingsModel
```

#### Сохранение настроек чатов

Настройки отдельных чатов (включён/выключен, расписание работы) автоматически сохраняются в JSON-файл и восстанавливаются после перезапуска бота:

```python
CHAT_SETTINGS_FILE = BASE_DIR.joinpath("data", "chat_settings.json")
CHAT_SETTINGS_PERSIST = True
```

Файл `data/chat_settings.json` создаётся автоматически при первом изменении настроек чата (например, после команды «выкл бот»). Значения из `CHAT_SETTINGS` в `settings.py` используются как начальные; сохранённые в файле настройки имеют приоритет.

## 🧪 Тесты

```bash
pip install -e .
python -m unittest discover -s tests -p "test_*.py" -v
```

Тесты запускаются в CI на Python 3.9–3.13 (GitHub Actions и Azure Pipelines).

## 💻 Пример работы

Бот по имени "Ходор" - [клик-клик (вк)](https://vk.com/hodor_designer)

## 🧰 CLI Shablbot

Для бота разработано CLI. Доступные методы:

```console
(env) C:\Users\user\Desktop\shablbot>py manager.py --help
usage: python manage.py  [-h] [-r] [-i] [-c]

🤖 Бот написанный на Python для социальной сети Вконтакте, работающий через VkBotLongPull

optional arguments:
  -h, --help       show this help message and exit
  -r, --run-bot    Запустить сервер для работы бота
  -i, --init       Инициировать каталоги для работы бота [ "commands", "keyboards", "modules", "phrases", "settings", "manager.py" ]
  -c, --check-bot  Проверить работоспособность бота без запуска сервера

(c) Alex Drachenin
```

> Примечание: флаги `--run-bot`, `--init` и `--check-bot` также доступны через `python -m shablbot`.

Для старта работы с ботом вы можете воспользоваться методом "--init" таким образом:
```console
(env) C:\Users\user\Desktop\shablbot>py -m shablbot --init

Каталог 'commands' инициирован!
Каталог 'keyboards' инициирован!
Каталог 'modules' инициирован!
Каталог 'phrases' инициирован!
Каталог 'settings' инициирован!
Файл manager.py инициирован!

```


## ❔ Как получить токен для работы бота? <a name="how_get_bot_token"></a>

Для начала нам нужно создать сообщество. Для этого переходим в вк в вкладку "<b>Сообщества</b>" и нажимаем кнопку "<b>Создать сообщество</b>".

Там вы заполняете всю необходимую вам информацию, со всем соглашаетесь и попадаете на страницу группы. Там нам нужно найти вкладку "<b>Управление</b>". В меню справа найдите "<b>Настройки</b>"->"<b>Работа с API</b>".

На той странице будет 3 вкладки. Из них нам нужны только 1 и 3:

1. Нажимаем кнопку "<b>Создать ключ</b>", выбираем все необходимые нам доступы (желательно все) и нажимаем "<b>Создать</b>". Данный ключ нужен для переменной [TOKEN](#start_setting) в настройках бота.
2. Не нужна, пропускаем ее.
3. На данной вкладке вам нужно выбрать версию API, бот тестировался на самом последней версии в момент написания (5.131), советую выбирать самую свежую. Так же вам нужно установить "<b>Long Poll API</b>" в значение "<b>Включено</b>". После этого переходим на вкладку "<b>Тип событий</b>" и выбираем нужные вам значения. Минимальные для работы бота:
   1. Входящее сообщение
   2. Исходящее сообщение

После этого ваш бот готов к работе, можете начинать его тестировать, удачи!

## ✍️ Автор
* [@alex_blackgard](https://vk.com/alexblackgard) - создатель бота и человек, который будет рад любой помощи в доработке бота  🐙💭🌎

<div align="center">

[![vk](./images/vk.svg)](https://vk.com/alexblackgard) [![instagram](./images/instagram.svg)](https://www.instagram.com/alexandr_blackgard/) [![github](./images/github.svg)](https://github.com/Blackgard)

</div>
