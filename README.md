# <img alt="bot-icon" src="https://image.flaticon.com/icons/svg/1786/1786548.svg" width="40px"></img>&nbsp;ShablBot
![Build](https://img.shields.io/azure-devops/build/sasna142/shablbot/2)
![License](https://img.shields.io/github/license/blackgard/shablbot)
<br>

Бот для социальной сети Вконтакте, работающий через VkBotLongPull (Через сообщество вконтакте).

# Установка
```
  git clone https://github.com/Blackgard/vk-bot-python.git
```

# Настройка бота 
Все для регулировки бота находится в файле **settings.py**.

Обязательные поля для работы бота:
  1. *token* - Ключ доступа к сообществу вконтакте, обязательно ключ должен быть с правами к сообщениям сообщества.
  2. *bot_group_id* - Id сообщества, от лица которого будет работать бот.
  3. *def_temp* - Слово на которое бот будет обязательно как-либо реагировать.
  4. *admin_id* - Id человека, от лица которого будет происходить администирование бота.
  
Остальные параметры для начального запуска бота менять не нужно.

# Запуск бота

```
  windows : python run_bot.py
  linux   : python3 run_bot.py
```
