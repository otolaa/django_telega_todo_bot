from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, HttpRequest
from django.views.decorators.http import require_POST, require_GET
import telebot
import logging
import json, sys, os, time  
from config.settings import BOT_TOKEN, ADMIN_CHAT_ID, STATIC_DIR

from .models import *


version_relise = '0.0.1'
bot = telebot.TeleBot(BOT_TOKEN, threaded = False,  parse_mode = 'HTML')

logging.basicConfig(
    level = logging.DEBUG, 
    filename = f'{STATIC_DIR}/text.log', 
    format = "%(asctime)s - %(module)s - %(levelname)s - %(funcName)s: %(lineno)d - %(message)s", 
    datefmt = '%H:%M:%S',
)

logger = logging.getLogger(__name__)

def main_view(request):
    response = JsonResponse({
        'ok':True, 'result':True, 
        'method':request.method, 'v':version_relise,
    })
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, OPTIONS"
    response["Access-Control-Allow-Headers"] = "X-Requested-With, Content-Type"

    return response  

def get_name(message):
    name = f'{message.from_user.first_name}'
    if message.from_user.last_name is not None: 
        name = f'{message.from_user.first_name} {message.from_user.last_name}'
    
    return name

@require_POST
def api_bots(request: HttpRequest, token):
    """ main function """
    try:  
        method = request.method  
        data_unicode = request.body.decode('utf-8')

        if data_unicode is None or data_unicode is '':
            return JsonResponse({'error':True, 'method':method})

        data = json.loads(data_unicode)
        update = telebot.types.Update.de_json(data)
        bot.process_new_updates([update])

    except Exception as e:
        logger.error(sys.exc_info()[1])        

    return main_view(request)

@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    name = get_name(message)
    bot.send_message(message.chat.id, f'Приветствуем Вас! {name}\n'
                                      f'Это ТоДо-Бот, для списка дел!?\n'
                                      f'Чтобы узнать больше команд, напишите /help')

@bot.message_handler(commands=['getinfo'])
def getchatid(message: telebot.types.Message):
    mess = [
        f'cid: {message.chat.id}',
        f'mid: {message.message_id}',
        f'uid: {message.from_user.id}',
        f'name: {message.from_user.first_name}',
        f'ver: {version_relise}'
    ]

    bot.send_message(message.chat.id, '\n'.join(mess))

@bot.message_handler(content_types=["text"])
def echo_messages(message: telebot.types.Message):
    bot.send_message(message.chat.id, message.text)