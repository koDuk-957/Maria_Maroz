# Мария Мароз — Telegram-бот и визитка

Проект содержит Telegram-бота на aiogram 3, страницу-визитку и Telegram Mini App.

## Локальный запуск

Требуется Python 3.10 или новее.

1. Установите зависимости:

   ```bash
   pip install -r requirements.txt
   ```

2. Скопируйте `.env.example` в `.env` и укажите собственный токен бота от @BotFather:

   ```env
   BOT_TOKEN=вставьте_сюда_новый_токен
   CONTACT_USERNAME=Maroz_Maria
   MINIAPP_URL=
   ```

   Не публикуйте токен в GitHub и не отправляйте его в переписке. Если токен когда-либо попал в публичный репозиторий, отзовите его через @BotFather и выпустите новый.

3. Запустите приложение:

   ```bash
   python main.py
   ```

   Приложение использует webhook и требует публичный HTTPS-адрес. Для локальной разработки настройте HTTPS-туннель и переменную `RENDER_EXTERNAL_URL` либо используйте отдельную локальную конфигурацию.

## Развёртывание на Render

Создайте **Web Service** с настройками:

- Build Command: `pip install -r requirements.txt`
- Start Command: `python main.py`
- Instance Type: `Free`

Добавьте Environment Variables:

- `BOT_TOKEN` — новый токен от @BotFather.
- `CONTACT_USERNAME` — `Maroz_Maria`.

Render автоматически предоставляет `RENDER_EXTERNAL_URL` и `PORT`. При запуске приложение регистрирует Telegram webhook и обслуживает проверку состояния по адресу `/health`.

Бесплатный Web Service может засыпать при отсутствии входящих запросов, поэтому возможны задержки при первом обращении после простоя.

## Сайт и Mini App

Файлы `index.html` и `miniapp.html` — статические страницы. Разместите их отдельно на публичном HTTPS-хостинге, например Cloudflare Pages. После публикации укажите полный адрес `miniapp.html` в переменной `MINIAPP_URL`, чтобы добавить кнопку открытия Mini App в Telegram.

## Структура

- `main.py` — запуск веб-сервиса и Telegram webhook.
- `handlers.py` — команды и обработчики кнопок.
- `keyboards.py` — клавиатуры Telegram.
- `services_data.py` — описания услуг и пункты меню.
- `config.py` — переменные окружения.
- `index.html` — веб-визитка.
- `miniapp.html` — Telegram Mini App.
