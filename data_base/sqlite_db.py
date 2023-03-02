import sqlite3
from ozon import *



def sql_start():
    global connectSellersDb, cursorSellersDb,connectAdminsDb,cursorAdminsDb
    connectSellersDb = sqlite3.connect('sellers.db')
    cursorSellersDb = connectSellersDb.cursor()
    print('Data base connected!')
    cursorSellersDb.execute('''CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_tg INT, 
        login_tg TEXT,
        country TEXT,
        ozon_client_id TEXT,
        ozon_api_key TEXT,
        trial BOOL,
        auth BOOL);
        ''')
    connectSellersDb.commit()
    #
    connectAdminsDb = sqlite3.connect('admins.db')
    cursorAdminsDb = connectAdminsDb.cursor()
    print('Data base connected!')
    cursorAdminsDb.execute('''CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_tg INT, 
        login_tg TEXT,
        country TEXT);
        ''')
    connectAdminsDb.commit()

    
#Заполнение бд           
def createAdminsDb(personId,username,country):
    cursorAdminsDb.execute(f'SELECT id_tg FROM users WHERE id_tg = {personId};')
    if cursorAdminsDb.fetchone() is None:
        cursorAdminsDb.execute(f'INSERT INTO users(id_tg,login_tg,country) VALUES(?,?,?);',(personId,username,country))
        connectAdminsDb.commit()
    else:
        connectAdminsDb.commit()
        
def createUsersDb(personId,username,country):
    cursorSellersDb.execute(f'SELECT id_tg FROM users WHERE id_tg = {personId};')
    if cursorSellersDb.fetchone() is None:
        cursorSellersDb.execute(f'INSERT INTO users(id_tg,login_tg,country,trial,auth) VALUES(?,?,?,?,?);',(personId,username,country,0,0))
        connectSellersDb.commit()
    else:
        connectSellersDb.commit()
        
#Проверка бесплатного доступа к боту
def checkTrial(personId):
    cursorSellersDb.execute(f'''SELECT trial FROM users WHERE id_tg = {personId};''')
    trial = cursorSellersDb.fetchone()
    if trial[0] == 0:
        response = 'Вам доступен бесплатный тест бота на 24 часа!'
    else:
        response = 'Вы уже использовали бесплатный тест. Купите подписку!'
    cursorSellersDb.execute(f'SELECT ozon_client_id FROM users WHERE id_tg = {personId};')
    ozon_client_id = cursorSellersDb.fetchone()
    cursorSellersDb.execute(f'SELECT ozon_api_key FROM users WHERE id_tg = {personId};') 
    ozon_api_key = cursorSellersDb.fetchone()
    connectSellersDb.commit()   
    return (response,ozon_client_id[0],ozon_api_key[0])
#Изменение client id, api key
def changeSellerApiKey(clientId,apiKey,personId):
    response = auth(clientId,apiKey)
    if response:
        cursorSellersDb.execute(f'UPDATE users SET ozon_client_id = ?,ozon_api_key = ?,auth = ? WHERE id_tg = {personId};',(clientId,apiKey,1))
        connectSellersDb.commit()
        return True
    else:
        return False
#Парсинг токенов
def parseOzonTokens(id):
    ozon_client_id = (cursorSellersDb.execute(f'SELECT ozon_client_id FROM users WHERE id_tg = {id}')).fetchone()
    ozon_api_key = (cursorSellersDb.execute(f'SELECT ozon_api_key FROM users WHERE id_tg = {id}')).fetchone()
    connectSellersDb.commit()
    return ozon_client_id,ozon_api_key
#Проверка на аутентификацию озона
def checkAuth(id):
    response = (connectSellersDb.execute(f'SELECT auth FROM users WHERE id_tg = {id}')).fetchone()
    if response[0] == 1:
        return True
    else:
        return False
