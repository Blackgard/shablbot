# Ходор — VK-бот на ShablBot

Готовый деплой бота в образе **Ходора** из «Игры престолов».

## Быстрый старт на сервере

```bash
git clone https://github.com/Blackgard/shablbot.git
cd shablbot/deploy/hodor
cp .env.example .env
nano .env   # заполните TOKEN, BOT_CHAT_ID, ADMIN_ID, API-ключ
./deploy.sh
```

Health-check (для nginx на порту 3010):

```bash
curl http://127.0.0.1:3010/
# {"status": "ok", "character": "hodor", ...}
```

## .env — что заполнить

| Переменная | Описание |
|------------|----------|
| `TOKEN` | Токен VK-сообщества |
| `BOT_CHAT_ID` | ID сообщества |
| `ADMIN_ID` | Ваш VK ID |
| `OPENROUTER_API_KEY` или `POLZA_API_KEY` | Ключ нейросети |
| `AI_PROVIDER` | `openrouter` или `polza` |
| `AI_MODEL` | Модель, например `openai/gpt-4o-mini` |

Остальное уже настроено под Ходора.

## Без Docker (systemd)

```bash
./install-systemd.sh
sudo systemctl status shablbot-hodor
```

## Nginx

Пример конфига: `nginx.conf.example` — прокси на `127.0.0.1:3010`.

## Поведение бота

- **Личка:** отвечает на любое сообщение (AI standalone)
- **Беседы:** реагирует на «ходор», «hodor», «бот»
- **Фразы:** «Ходор», «Hodor!» и вариации
- **Команды:** «выключи бота», «помоги» — через нейросеть
