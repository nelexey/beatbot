import requests
import config
import db_handler


bot_token = config.TOKEN

# Список chat_ids, которым нужно отправить сообщение
chat_ids = db_handler.get_all_chat_ids()

message_text = '''Привет! 👋 

Может быть, стоит обратить внимание на наши новые бесплатные опции?

Или даже посмотреть на обновленную генерацию битов? 🎹'''

# URL для отправки сообщения через API Telegram Bot
api_url = f'https://api.telegram.org/bot{bot_token}/sendMessage'

# Отправка сообщения каждому chat_id из списка
for chat_id in chat_ids:
    data = {
        'chat_id': chat_id,
        'text': message_text
    }

    response = requests.post(api_url, data=data)

    if response.status_code == 200:
        print(f'Сообщение успешно отправлено пользователю с chat_id {chat_id}')
    else:
        print(f'Ошибка при отправке сообщения пользователю с chat_id {chat_id}: {response.status_code}')
        print(response.text)
