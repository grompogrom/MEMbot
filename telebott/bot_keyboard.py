from telebot import types

start_keyboard = types.InlineKeyboardMarkup()
item_ID = types.InlineKeyboardButton(text='ID Сервера дискорд', callback_data='ID')
item_rec_voice = types.InlineKeyboardButton(text='Записать прикол', callback_data='rec_voice')
start_keyboard.add(item_ID,item_rec_voice)

rec_keyboard = types.InlineKeyboardMarkup()
item_remove = types.InlineKeyboardButton(text='Перезаписать', callback_data='rec_voice')
item_confirm = types.InlineKeyboardButton(text='Сохранить', callback_data='save_voice')
item_cancel = types.InlineKeyboardButton(text='Отмена', callback_data='cancel')
rec_keyboard.add(item_cancel,item_remove, item_confirm)