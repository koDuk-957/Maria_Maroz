# Мария Мароз — Telegram-бот и визитка

Проект содержит Telegram-бота на aiogram 3, сайт-визитку и Telegram Mini App.

## Локальный запуск

Требуется Python 3.12.10.

1. Установите зависимости:

   ```bash
   pip install -r requirements.txt
   ```

2. Скопируйте `.env.example` в `.env` и укажите токен бота от @BotFather:

   ```env
   BOT_TOKEN=вставьте_сюда_новый_токен
   CONTACT_USERNAME=Maroz_Maria
   MINIAPP_URL=https://maria-maroz.onrender.com/miniapp
   ```

   Не публикуйте токен в GitHub и не отправляйте его в переписке. Если токен когда-либо попадал в публичный репозиторий, отзовите его через @BotFather и выпустите новый.

3. Запустите приложение:

   ```bash
   python main.py
   ```

   Для локальной работы webhook нужен публичный HTTPS-адрес и переменная `RENDER_EXTERNAL_URL`.

## Развёртывание на Render

Создайте **Web Service** со следующими настройками:

- Build Command: `pip install -r requirements.txt`
- Start Command: `python main.py`
- Instance Type: `Free`

Добавьте Environment Variables:

- `BOT_TOKEN` — действующий токен от @BotFather.
- `CONTACT_USERNAME` — `Maroz_Maria`.
- `MINIAPP_URL` — `https://maria-maroz.onrender.com/miniapp`.

Render автоматически предоставляет `RENDER_EXTERNAL_URL` и `PORT`. При запуске приложение регистрирует Telegram webhook.

## Адреса

- Сайт-визитка: `https://maria-maroz.onrender.com/`
- Telegram Mini App: `https://maria-maroz.onrender.com/miniapp`
- Проверка сервиса: `https://maria-maroz.onrender.com/health`

Страницы `index.html` и `miniapp.html` обслуживаются самим приложением через `main.py`; отдельный статический хостинг не требуется.

Бесплатный Render Web Service может засыпать при отсутствии запросов. После простоя первый запуск может задержаться, поэтому бесплатный тариф не гарантирует мгновенную доступность 24/7.

## Структура

- `main.py` — запуск веб-сервиса и Telegram webhook.
- `handlers.py` — команды и обработчики Telegram.
- `keyboards.py` — клавиатуры Telegram.
- `services_data.py` — единый источник описаний услуг и пунктов меню.
- `config.py` — переменные окружения.
- `index.html` — веб-визитка.
- `miniapp.html` — Telegram Mini App.
- `tests/test_project.py` — smoke-тесты меню и карточек услуг.
