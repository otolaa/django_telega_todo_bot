# from django.shortcuts import render
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse, HttpRequest
from django.views.decorators.http import require_POST, require_GET
import telebot
import logging
import json, sys, os, time
from .great import GreatTodo, add_teg
from config.settings import BOT_TOKEN, ADMIN_CHAT_ID, STATIC_DIR

from .models import *


version_relise = 0.1
bot = telebot.TeleBot(BOT_TOKEN, threaded = False,  parse_mode = 'HTML')
suffix = '🌻'
separator = '~' * 25

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

        if data_unicode == None or data_unicode == '':
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
    mess = [
        f'Приветствуем Вас! ' + suffix,
        f'{name}',
        separator,
        f'Это ТоДо-Бот, для списка дел',
        separator,
        f'Добавить - /add Ваше дело!',
        f'Получить список - /list',
        separator,
        f'Узнать больше - /help',
    ]
    bot.send_message(message.chat.id, '\n'.join(mess))

@bot.message_handler(commands=['help'])
def help(message: telebot.types.Message):
    mess = [
        f'/start - включить бота',        
        # f'/getinfo - информация',
        f'/list - список дел',
        f'/add - добавляет дело', 
        f'/help - справочник',       
    ]
    bot.send_message(message.chat.id, '\n'.join(mess))

@bot.message_handler(commands=['add'])
def add_todo(message: telebot.types.Message):
    """ add """
    mess = []
    s = message.text.replace('/add', '', 1)
    s = s.strip()

    Gt = GreatTodo(uid=message.from_user.id, username=message.from_user.username)
    id_or_bool = Gt.add(s=s)
    if id_or_bool is False:
        mess.append(' ~ '.join(Gt.error))
    else:
        mess.append(f'Успешно добавлено - №{id_or_bool}')

    bot.send_message(message.chat.id, '\n'.join(mess))

@bot.message_handler(commands=['getinfo'])
def getchatid(message: telebot.types.Message):
    mess = [
        f'@{message.from_user.username}',
        f'{get_name(message)}',
        separator,
        f'cid: {message.chat.id}',
        f'mid: {message.message_id}',
        f'uid: {message.from_user.id}',        
        separator,
        f'ver: {version_relise}'
    ]

    bot.send_message(message.chat.id, '\n'.join(mess))

@bot.message_handler(commands=['list'])
def list_items(message: telebot.types.Message, page:int = 1, update_message:bool = False):
    mess = []
    uid = message.from_user.id
    list_todo = Todo.objects.filter(uid=uid).order_by('-created_at')[:100]
    if len(list_todo) == 0:
        bot.send_message(message.chat.id, f'дел нету, добавте /add')

    pg = Paginator(list_todo, 1)
    page_item = pg.page(page)

    for item in page_item.object_list:
        t_format = item.created_at.strftime("%d.%m.%y %H:%M")
        is_active = f'{"✅" if item.is_active is True else "❎"}'
        res = [
            add_teg(text_str=f'№{item.id} ~ {t_format} ~ ', tegs=['b']) + is_active,
            f'{item.title}',
        ]

        mess.append('\n'.join(res))

    types = telebot.types
    buttons = types.InlineKeyboardMarkup()

    left  = page-1 if page != 1 else pg.num_pages
    right = page+1 if page != pg.num_pages else 1

    left_button  = types.InlineKeyboardButton("←", callback_data=f'to_{left}_{uid}')
    page_button  = types.InlineKeyboardButton(f"{str(page)}/{str(pg.num_pages)}", callback_data='_') 
    right_button = types.InlineKeyboardButton("→", callback_data=f'to_{right}_{uid}')
    buttons.add(left_button, page_button, right_button)

    buy_button   = types.InlineKeyboardButton("❌", callback_data=f'dell_{uid}')
    buttons.add(buy_button)

    if update_message is False:
        bot.send_message(message.chat.id, '\n'.join(mess), disable_web_page_preview=True, reply_markup=buttons)
    else:
        bot.edit_message_text('\n'.join(mess), message.chat.id, message.message_id, disable_web_page_preview=True, reply_markup=buttons)

@bot.callback_query_handler(func=lambda c: True)
def callback(c):
    """ handler callback """
    f = str(c.data)
    if f.find('to_') >= 0:
        list_param = f.split("_")
        page = int(list_param[1])
        c.message.from_user.id = list_param[2] # update uid
        list_items(message=c.message, page=page, update_message=True)