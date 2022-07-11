from dotenv import load_dotenv
from pathlib import Path
import os
from flask import Flask, request
import telegram

load_dotenv(Path(".env"))
TOKEN = os.getenv('bot_token')
bot = telegram.Bot(token=TOKEN)
app = Flask(__name__)

@app.route('/{}'.format(TOKEN), methods=['POST'])
def respond():
