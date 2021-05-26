import telebot
import requests
from bot_keyboard import start_keyboard, rec_keyboard
import servers_users
import const
from voice_opt import voice_record
import check_connection

bot = telebot.TeleBot(const.TG_TOKEN)
voice_cash = {}


@bot.message_handler(commands=['get_info', 'info', 'help', 'start'])
def start_info(message):
    dell_last_msg()

    chat_id = message.from_user.id
    user_name = message.from_user.username
    global last_msg
    last_msg = bot.send_message(chat_id,
                                f'Привет, {user_name}! Я... Да не важно кто. ' +
                                'Ты можешь рассказывать мне рофлы, а я поделюсь ими с твоими друзьями в дискорде',
                                reply_markup=start_keyboard)

    print(last_msg.from_user.id, ' ', last_msg.message_id)


@bot.message_handler(content_types=['text'])
def get_text_mess(message):
    dell_last_msg()
    global last_msg
    chat_id = message.from_user.id
    if message.text.lower() == 'привет':
        bot.send_message(chat_id, 'Здоров от Макса')
    else:
        last_msg = bot.send_message(message.from_user.id,
                                    'Поделишься чем-нибудь?',
                                    reply_markup=start_keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    print(call.from_user.username, call.data)
    dell_last_msg()
    chat_id = call.from_user.id
    if call.data == 'ID':
        if chat_id in user_ds_id:
            print('[log] waitng for id')
            msge = bot.send_message(chat_id,
                                    f'Сейчас id твоего сервера {user_ds_id[call.from_user.id]}. Отправь мне новый id ')
        else:
            print('[log] waiting for id')
            msge = bot.send_message(chat_id,
                                    'Отправь мне ID своего дискорд сервера, чтобы я рассказал это твоим друзьм )')
        bot.register_next_step_handler(msge, process_get_dsid)
    elif call.data == 'rec_voice':
        if chat_id in user_ds_id:
            msge = bot.send_message(chat_id, 'Ну, рассказывай')
            bot.register_next_step_handler(msge, process_check_voice)
        else:
            msge = bot.send_message(chat_id, 'Введи-ка ты сперва id discord сервера ')
            bot.register_next_step_handler(msge, process_get_dsid)
    elif call.data == 'save_voice':
        saveVoice(call)
    elif call.data == 'cancel':
        pass


def process_check_voice(message):
    global last_msg
    chat_id = message.from_user.id
    if message.content_type == 'voice':
        file_info = bot.get_file(message.voice.file_id)
        file = requests.get(
            f'https://api.telegram.org/file/bot{const.TG_TOKEN}/{file_info.file_path}')
        voice_cash[chat_id] = (file.content, message.date)
        last_msg = bot.send_voice(message.from_user.id, file.content, reply_markup=rec_keyboard)
    else:
        msg = bot.send_message(chat_id, 'Дурашка ) Отправь голосовое сообщение')
        bot.register_next_step_handler(msg, process_check_voice)


def saveVoice(call):
    global last_msg
    chat_id = call.from_user.id
    user_name = call.from_user.username
    voice_date = voice_cash[chat_id][1]
    file = voice_cash[chat_id][0]
    print(voice_date)
    voice_record(user_name, voice_date, file, user_ds_id[chat_id])
    del voice_cash[chat_id]

    bot.send_message(chat_id, 'Ахахаха, я запомнил')
    last_msg = bot.send_message(chat_id,
                                'Ну, есть новые рофлы?',
                                reply_markup=start_keyboard)


def process_get_dsid(message):
    global last_msg
    try:
        chat_id = message.from_user.id
        if len(message.text) == 18:
            if chat_id not in user_ds_id:
                user_ds_id[chat_id] = message.text
            else:
                del user_ds_id[chat_id]
                user_ds_id[chat_id] = message.text
            servers_users.save_serversID(user_ds_id)
            bot.send_message(chat_id, 'ID успешно сохранен')
            last_msg = bot.send_message(chat_id,
                                        'Я бот для анекдотов, принимаю ваши приколы, а затем вывожу их в дискорд',
                                        reply_markup=start_keyboard)
        else:
            last_msg = bot.send_message(chat_id, 'Чееее? это не ID')
            bot.register_next_step_handler(last_msg, process_get_dsid)
    except Exception:
        print('Ошибка добавления')


def dell_last_msg():
    try:
        bot.delete_message(last_msg.chat.id, last_msg.message_id)
    except Exception:
        pass


try:
    user_ds_id = servers_users.get_serversID()
except Exception:
    user_ds_id = {}
    print('Ошибка в загрузке user_ds_id')


def start():
    try:
        bot.polling(none_stop=True, interval=0)
    except Exception:
        check_connection.connection()
        start()


start()
