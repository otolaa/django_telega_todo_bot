# тг. бот списка дел
```
в файле .env  токен и chat_id администратора-менеджера
```

## Django + Webhook + pyTelegramBotAPI

```
$ cp .env.example .env
```

```
$ pip install -r requirements.txt
```

## Сервис для проброса тунеля pinggy.io
позволяет тестировать bot на setWebhook
```
ssh -p 443 -R0:localhost:8000 qr@a.pinggy.io
```

## api на Django для bota
pinggy - возвращает url который будит вашим api для телеграм бота
```
toket_you_bot = ''
api_from_telegram = https://rnacj-147-45-240-74.a.free.pinggy.link/todo/{toket_you_bot}/
```

## установить setWebhook для бота
```
https://api.telegram.org/bot{toket_you_bot}/setWebhook?url=https://rnacj-147-45-240-74.a.free.pinggy.link/todo/{toket_you_bot}/
```