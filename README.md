<p align="center">
  <a href="" rel="noopener">
 <img width=100px height=100px src="https://image.flaticon.com/icons/svg/1786/1786548.svg" alt="Project logo"></a>
</p>

<h3 align="center">ShablBot</h3>

![Build](https://img.shields.io/azure-devops/build/sasna142/026fd26f-bb59-48fd-bb91-6d9ebe113f87/2)
![License](https://img.shields.io/github/license/blackgard/shablbot)

---------------------------------

 🤖 Бот написанный на Python для социальной сети Вконтакте, работающий через VkBotLongPull. 

## 🎈 Установка
```
  git clone https://github.com/Blackgard/shablbot.git
```

## 🏁 Настройка бота 
Все для регулировки бота находится в файле **settings.py**. Для каждой переменной в файле есть подробное описание ее возможностей.

Обязательные поля для работы бота:
1. *token* - ключ доступа к сообществу вконтакте, ключ должен быть с правами к сообщениям сообщества.
``` 
  token       = r'1234566789908798689764867293876243987" # (str)
```
2. *bot_group_id* - id страницы вконтакте сообщества, от лица которого будет работать бот.
```
  bot_chat_id = 123456789  # (int)
```
3. *def_temp* - слово на которое бот будет как-либо реагировать.
```
  def_templ       = [             
        r"бот",
  ]     
```
4. *admin_id* - id страницы вконтакте человека, от лица которого будет происходить администрирование бота.
```
  admin_id        = 123456789 # (int)
```
Остальные параметры для начального запуска бота менять не нужно.

## 🚀 Запуск бота

```
  windows : py run_bot.py
  linux   : python run_bot.py
```

## 💻 Пример работы 

Бот по имени "Ходор" - <a href='https://vk.com/hodor_designer'>vk.com/hodor_designer</a>

## ✅ Методы 

Файл **cache.py**:
* `save_chat_to_cache(chat_id, settings = None)` : задает начальные правила для работы бота с новой беседой.
* `add_word_in_counter_chat(chat_id, type_word)` : добавляет группе, в которую бот отправил сообщение, редкость отправленной фразы.

Файл **chat_settings**
* `get_settings_chat(chat_id, type_time = None, t_from = None, t_to = None, included = None)` : по переданным параметрам создает настройки для беседы, с которой бот взаимодействовал.
* `modify_settings_chat(chat_id, settings)` : изменяет настройки у заданной группы на те, которые переданны переменной settings.

Файл **handler_command**
* `parse_message_com(message, user_id, chat_id, botAPI)` : ищет в полученном ботом сообщении ключевые слова, означающие команду для бота.
* `execute_public_com(name_com, chat_id, admin_id=SETTINGS.admin_id)` : обратывает публичные команды и возращает для каждой команды свой ответ.
* `execute_private_com(command, name_com, bot, chat_id, admin_id=SETTINGS.admin_id)` : обратывает приватные команды и возращает для каждой команды свой ответ.

Файл **handler_message**
* `get_random_id()` : возращает случайное число (необходимо для отправки сообщения).
* `write_msg(answer, chat_id, botAPI)` : осуществляет отправку сообщения пользователю или в беседу.
* `choice_of_answer(found_matches)` : осуществляет выбор ответа из найденных в сообщении ключевых слов.
* `find_matches(message)` : производит поиск в сообщении ключевых слов.
* `preprocessing_message(list_answer, chat_id, botAPI)` : производит обработку сообщения перед отправкой (В следующей версии будет удалена)
* `check_on_com_and_module(message, eventObj, botAPI)` : мост между файлами handler_command и handler_modules.
* `handler_message(eventObj, chat_id, botAPI)` : входная точка обработки сообщения.

Файл **handler_modules**
* `parse_message_module(message, user_id, chat_id, botAPI)` : ищет в полученном ботом сообщении ключевые слова, для выполнения функционала модулей.
* `find_mathes(message, templates)` : производит поиск в сообщении ключевых слов. (В следующей версии будет удалена).

Файл **init_bot**
* `check_module(module_path)` : ищет модуль для импортирования по указанному пути.
* `import_module_from_spec(module_spec)` : производит импортирование модуля по полученному spec из функции check_module.
* `load_cache()` : производит загрузку в кеш бота данных из файла settings.py.
* `load_modules()` : производит загрузку модуле.
* `init_components()` : входная точка инициализации бота.

Файл **time_work**
* `_getTime(time)` : создает по переданной строке со временем обьект datetime.
* `check_work_time(chat_id)` : проверяет может имеет ли бот писать ответ в беседу.

## ✍️ Автор
* [@alex_blackgard](https://github.com/blackgard) - bot creator
