# Koyeb Deploy

Цей бот підготовлений під деплой на `Koyeb` як `Worker`.

## Що вже готово

- `Dockerfile` для автоматичної збірки
- токени читаються зі змінних середовища
- `env.example` як шаблон

## Як залити

1. Завантаж код у GitHub репозиторій.
2. У Koyeb створи новий App.
3. Обери `GitHub` як source.
4. Обери репозиторій з ботом.
5. Тип сервісу: `Worker`.
6. Builder: `Dockerfile`.
7. Додай environment variables:
   - `BOT_TOKEN`
   - `CRYPTOBOT_TOKEN`
   - `ADMIN_IDS`
8. Deploy.

## Важливо

- Бот використовує `users_data.json`.
- На безкоштовних хостингах файлове сховище часто тимчасове.
- Після redeploy або restart частина локальних даних може скинутись.
- Для стабільного продакшену краще потім винести дані в БД.

## Корисні адмін-команди

- `/vip_grant USER_ID`
- `/vip_revoke USER_ID`
- `/vip_free USER_ID`
- `/stats`
- `/broadcast текст`
