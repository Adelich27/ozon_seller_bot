from aiogram import types, Dispatcher
from aiogram.types.reply_keyboard import ReplyKeyboardMarkup
from create_bot import dp, bot
from keyboards import markupSubcribed,sellerKeyboard,markupSettings
from aiogram.types import ReplyKeyboardRemove
from data_base import sqlite_db
from tokens import channelId
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State,StatesGroup
from ozon import *
import time

async def checkUserStatusChannel(info):
    return True if info['status'] != 'left' else False

# user already subcribed
async def start(message: types.Message):
    sqlite_db.createUsersDb(message.from_user.id,f'@{message.from_user.username}',message.from_user.language_code)
    if await checkUserStatusChannel(await bot.get_chat_member(channelId,message.from_user.id)):
        tgName = message.from_user.first_name
        trial = sqlite_db.checkTrial(message.from_user.id)
        response = await bot.get_chat_administrators(chat_id=channelId)
        #check admin
        if message.from_user.id == response[0]['user']['id']:
            # выдать админ клаву
            sqlite_db.createAdminsDb(message.from_user.id,f'@{message.from_user.username}',message.from_user.language_code)
            await bot.send_message(message.from_user.id,
        f'''
        Режим администратора 
        Рады тебя видеть, {tgName}!
        {trial[0]}
        Для того, чтобы пользоваться ботом укажи в настройках токены Ozon'а! Личный кабинет - Настройки
        Ваш client_id: {trial[1]}
        Ваш api_key: {trial[2]}

        ''')
        else: 
            await bot.send_message(message.from_user.id,
            f'''
            Рады тебя видеть, {tgName}!
            {trial[0]}
            Для того, чтобы пользоваться ботом укажи в настройках токены Ozon'а! Личный кабинет - Настройки
            Ваш client_id: {trial[1]}
            Ваш api_key: {trial[2]}
            ''',reply_markup=sellerKeyboard)

    else:
        await bot.send_message(message.from_user.id,"Сначала подпишись на канал!",reply_markup=markupSubcribed)
# user not subcribed 
async def checkSubscribe(query: types.CallbackQuery):
    await bot.delete_message(query.from_user.id,query.message.message_id)
    if await checkUserStatusChannel(await bot.get_chat_member(channelId,query.from_user.id)):
        tgName = query.from_user.first_name
        trial = sqlite_db.checkTrial(query.from_user.id)
        await bot.send_message(query.from_user.id,
        f'''
            Рады тебя видеть, {tgName}!
            {trial[0]}
            Для того, чтобы пользоваться ботом укажи в настройках токены Ozon'а! Личный кабинет - Настройки
            Ваш client_id: {trial[1]}
            Ваш api_key: {trial[2]}
            ''',reply_markup=sellerKeyboard)
    else:
        await bot.send_message(query.from_user.id,"Сначала подпишись на канал!",reply_markup=markupSubcribed)
# Реализация кнопки Личный кабинет
class fsmSettingsButton(StatesGroup):
    client_id = State()
    api_key = State()

async def sellerLk(message: types.Message):
        trial = sqlite_db.checkTrial(message.from_user.id)
        tgName = message.from_user.first_name
        await bot.send_message(message.from_user.id,
        f'''
        Личный кабинет
        ---
        Имя: {tgName}
        Ваш client_id: {trial[1]}
        Ваш api_key: {trial[2]}
        ''',reply_markup=markupSettings)
        
async def sellerLkSettings(query: types.CallbackQuery):
    await bot.send_message(query.from_user.id,"Введите client id")
    await fsmSettingsButton.client_id.set()
#Ловим 1 ответ по настройкам client id
async def loadClientId(message:types.Message,state: FSMContext):
    async with state.proxy() as data:
        data['client_id'] = message.text
    await fsmSettingsButton.next()
    await bot.send_message(message.from_user.id,"Введите api key")
#Ловим 2 ответ по настройкам api key
async def loadApiKey(message:types.Message,state: FSMContext):
    async with state.proxy() as data:
        data['api_key'] = message.text
    await state.finish()
    
    response = sqlite_db.changeSellerApiKey(data['client_id'],data['api_key'],message.from_id)
    if response:
        await bot.send_message(message.from_user.id,"Успешно!")
    else:
        await bot.send_message(message.from_user.id,"В каком то ключе допущена ошибка!")
        await sellerLk(message) 
    
# Реализация кнопки журнал заказов
async def orders(message: types.Message):
    responseAuth = sqlite_db.checkAuth(message.from_id)
    if responseAuth:
        responseDb = sqlite_db.parseOzonTokens(message.from_id)
        response = ordersHistory(responseDb[0][0],responseDb[1][0])
        #вывод заказов
        for i in range(5):
            await bot.send_message(message.from_user.id,
            f'''
            Заказ №{i}
            Магазин https://www.ozon.ru/seller/love-story-more-581144/tovary-dlya-vzroslyh-9000/?miniapp=seller_581144
            ---
            Номер отправления: {response['result'][i]['posting_number']}
            Дата заказа: {response['result'][i]['created_at']}
            Артикул товара: {response['result'][i]['products'][0]['offer_id']}
            Название товара: {response['result'][i]['products'][0]['name']}
            Цена товара: {response['result'][i]['products'][0]['price']} рублей
            Статус товара: {response['result'][i]['status']}
            ''')
            time.sleep(0.3)
    else:
        await bot.send_message(message.from_id,"Проверьте настройки токенов Озона!")
        await sellerLk(message)
#поиск по номеру заказа
class fsmOrder(StatesGroup):
    numberOrder = State()
async def searchOrders(message: types.Message):
    responseAuth = sqlite_db.checkAuth(message.from_id)
    if responseAuth:
        
        await bot.send_message(message.from_id,"Введите номер заказа:")
        await fsmOrder.numberOrder.set()
        
        
    else:
        await bot.send_message(message.from_id,"Проверьте настройки токенов Озона!")
        await sellerLk(message)
#ловим ответ
async def setOrderNumber(message:types.Message,state: FSMContext):
    async with state.proxy() as data:
        data['numberOrder'] = message.text
    await state.finish()
    responseDb = sqlite_db.parseOzonTokens(message.from_id)
    response = searchOrder(responseDb[0][0],responseDb[1][0],data['numberOrder'])
    if response == False:
        await bot.send_message(message.from_id,"Такого номера заказа не существует!")
        await sellerLk(message)
    else:
        await bot.send_message(message.from_user.id,
        f'''
        Магазин https://www.ozon.ru/seller/love-story-more-581144/tovary-dlya-vzroslyh-9000/?miniapp=seller_581144
        Заказ № {response['result']['posting_number']}
        Дата заказа: {response['result']['created_at']}
        Артикул товара: {response['result']['products'][0]['offer_id']}
        Название товара: {response['result']['products'][0]['name']}
        Цена товара: {int(float(response['result']['products'][0]['price']))} рублей
        Статус товара: {response['result']['status']}
        ''')
#список клиентов 
async def clientsList(message: types.Message):
    responseAuth = sqlite_db.checkAuth(message.from_id)
    if responseAuth:
        responseDb = sqlite_db.parseOzonTokens(message.from_id)
        response = ordersHistory(responseDb[0][0],responseDb[1][0])
        #вывод заказов
        for i in range(5):
            if response['result'][i]['analytics_data']['is_legal'] == False:
                face = 'Физическое лицо'
            else:
                face = 'Юридическое лицо'
            await bot.send_message(message.from_user.id,
            f'''
            Клиент №{i}
            Магазин https://www.ozon.ru/seller/love-story-more-581144/tovary-dlya-vzroslyh-9000/?miniapp=seller_581144
            ---
            Регион клиента (область): {response['result'][i]['analytics_data']['region']}
            Способ оплаты: {response['result'][i]['analytics_data']['payment_type_group_name']}
            Получатель: {face}
            Способ доставки получателя: {response['result'][i]['analytics_data']['delivery_type']}
            ''')
            time.sleep(0.3)
    else:
        await bot.send_message(message.from_id,"Проверьте настройки токенов Озона!")
        await sellerLk(message)
#список товаров
async def itemsList(message: types.Message):
    responseAuth = sqlite_db.checkAuth(message.from_id)
    if responseAuth:
        responseDb = sqlite_db.parseOzonTokens(message.from_id)
        response = itemsListOzon(responseDb[0][0],responseDb[1][0])
        for i in range(response['result']['total']):
            await bot.send_message(message.from_id,
            f'''
            Товар №{i}
            Магазин https://www.ozon.ru/seller/love-story-more-581144/tovary-dlya-vzroslyh-9000/?miniapp=seller_581144
            ---
            Артикул: {response['result']['items'][i]['offer_id']}
            ''')
            time.sleep(0.3)
    else:
        await bot.send_message(message.from_id,"Проверьте настройки токенов Озона!")
        await sellerLk(message)
#поиск карточки товара
class fsmCard(StatesGroup):
    numberCard = State()
async def searchCard(message: types.Message):
    responseAuth = sqlite_db.checkAuth(message.from_id)
    if responseAuth:
        await bot.send_message(message.from_id,"Введите артикул товара:")
        await fsmCard.numberCard.set()
    else:
        await bot.send_message(message.from_id,"Проверьте настройки токенов Озона!")
        await sellerLk(message)
#ловим ответ
async def setNumberCard(message:types.Message,state: FSMContext):
    async with state.proxy() as data:
        data['numberCard'] = message.text
    await state.finish()
    responseDb = sqlite_db.parseOzonTokens(message.from_id)
    response = searchCardOzon(responseDb[0][0],responseDb[1][0],data['numberCard'])
    if response == False:
        await bot.send_message(message.from_id,"Такого артикула не существует!")
        await sellerLk(message)
    else:
        await bot.send_message(message.from_user.id,
        f'''
        Название товара: {response['result']['items'][0]['name']}
        Артикул: {response['result']['items'][0]['offer_id']}
        Актуальная цена: {int(float(response['result']['items'][0]['marketing_price']))} рублей
        Главное фото: {response['result']['items'][0]['primary_image']}
        Остаток на складе: {response['result']['items'][0]['stocks']['present']}
        ''')
        
#регистрация функций для дальнейшей передачи
def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(start,commands = ['start'] )
    dp.register_callback_query_handler(checkSubscribe,text = "checkSubscribeButton")
    dp.register_message_handler(sellerLk,text = 'Личный кабинет')
    dp.register_message_handler(orders,text = 'Журнал заказов')
    dp.register_message_handler(searchOrders,text = 'Поиск по номеру заказа',state=None)
    dp.register_message_handler(clientsList,text = 'Список клиентов')
    dp.register_message_handler(itemsList,text = 'Список товаров')
    dp.register_message_handler(searchCard,text = 'Поиск по артикулу товара')
    dp.register_callback_query_handler(sellerLkSettings,text = "sellerLkSettings",state=None)
    dp.register_message_handler(loadClientId,state=fsmSettingsButton.client_id)
    dp.register_message_handler(loadApiKey,state=fsmSettingsButton.api_key)
    dp.register_message_handler(setOrderNumber,state=fsmOrder.numberOrder)
    dp.register_message_handler(setNumberCard,state=fsmCard.numberCard)