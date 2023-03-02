from aiogram.types import ReplyKeyboardMarkup,InlineKeyboardButton,InlineKeyboardMarkup


buttonSubscribe = InlineKeyboardButton("Подписаться! 😎",url='https://t.me/channeltewst')
buttonCheckSubscribe = InlineKeyboardButton("Проверить",callback_data= "checkSubscribe")
markupSubcribed = InlineKeyboardMarkup(row_width=1).add(buttonSubscribe).add(buttonCheckSubscribe)
