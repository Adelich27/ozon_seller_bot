from aiogram.types import ReplyKeyboardMarkup,InlineKeyboardButton,InlineKeyboardMarkup,KeyboardButton

#старт проверка подписки на канал
buttonSubscribe = InlineKeyboardButton("Подписаться! 😎",url='https://t.me/channeltewst')
buttonCheckSubscribe = InlineKeyboardButton("Проверить",callback_data= "checkSubscribeButton")
markupSubcribed = InlineKeyboardMarkup(row_width=1).add(buttonSubscribe).add(buttonCheckSubscribe)
#после старта вывод клавиатуры
sellerButtonLk = KeyboardButton("Личный кабинет")
sellerButtonOrdersHistory = KeyboardButton("Журнал заказов")
sellerButtonClients = KeyboardButton("Список клиентов")
sellerButtonItemsList = KeyboardButton("Список товаров")
sellerButtonOrderSearch = KeyboardButton("Поиск по номеру заказа")
sellerButtonItem = KeyboardButton("Поиск по артикулу товара")
sellerKeyboard = ReplyKeyboardMarkup(resize_keyboard=True)
sellerKeyboard.add(sellerButtonLk).row(sellerButtonOrdersHistory,sellerButtonClients,sellerButtonItemsList).row(sellerButtonItem,sellerButtonOrderSearch)
#инлайн личный кабинет - настройки
buttonSettingsLk = InlineKeyboardButton("Настройки",callback_data="sellerLkSettings")
markupSettings = InlineKeyboardMarkup().add(buttonSettingsLk)
