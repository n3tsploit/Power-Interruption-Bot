from dotenv import load_dotenv
from pathlib import Path
import os
from flask import Flask, request
import telegram

load_dotenv(Path(".env"))
TOKEN = os.getenv('bot_token')
URL = os.getenv('URL')
bot = telegram.Bot(token=TOKEN)
app = Flask(__name__)


@app.route('/{}'.format(TOKEN), methods=['POST'])
def respond():
    update = telegram.Update.de_json(request.get_json(force=True), bot)

    chat_id = update.message.chat_id
    message_id = update.message.message_id
    text = update.message.text.encode('utf-8').decode()

    print('got text message: ', text)

    if text == '/start':
        welcome_message = 'Welcome How may I help you'
        bot.sendMessage(chat_id=chat_id, text=welcome_message, reply_to_message=message_id)

    else:
        print('bye')

    return 'ok'


@app.route('/setwebhook', methods=['POST', 'GET'])
def set_webhook():
    s = bot.set_webhook(f'{URL}{TOKEN}')
    if s:
        return 'webhook setup ok'
    else:
        return 'webhook setup failed'


@app.route('/')
def index():
    return '.'


if __name__ == '__main__':
    app.run(threaded=True)
