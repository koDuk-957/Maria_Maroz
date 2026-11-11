# Мария Мароз — Telegram-бот и визитка

Проект содержит Telegram-бота на aiogram 3, страницу-визитку и Telegram Mini App.

## Запуск бота

Требуется Python 3.10 или новее.

1. Установите зависимости:

   ```bash
   pip install -r requirements.txt
   ```

2. Скопируйте `.env.example` в `.env` и укажите токен бота:

   ```env
   BOT_TOKEN=9073173569:AAEsi55AjMzZDmWMxPS_5esLJ6WK59tTwh8
   CONTACT_USERNAME=Maroz_Maria
   MINIAPP_URL=https://maria-maroz-bot.onrender.com
   ```

   `MINIAPP_URL` необязателен. Пока он пустой, бот работает без кнопки открытия Mini App.

3. Запустите:

   ```bash
   python main.py
   ```

   Старый способ запуска также поддерживается:

   ```bash
   python bot_simple.py
   ```

## Развёртывание

Для постоянной работы бота используйте worker/background service с командой `python main.py` и задайте переменные окружения `BOT_TOKEN`, `CONTACT_USERNAME` и при необходимости `MINIAPP_URL`. Файл `Procfile` содержит команду для worker.

Файлы `index.html` и `miniapp.html` — статические страницы. Чтобы открыть Mini App из Telegram, отдельно разместите `miniapp.html` на публичном HTTPS-хостинге и укажите его полный адрес в `MINIAPP_URL`. Сам Telegram-бот не раздаёт эти HTML-файлы.

## Структура

- `main.py` — основной запуск бота.
- `handlers.py` — команды и обработчики кнопок.
- `keyboards.py` — клавиатуры Telegram.
- `services_data.py` — описания услуг и пункты меню.
- `config.py` — переменные окружения.
- `index.html` — веб-визитка.
- `miniapp.html` — Telegram Mini App.
