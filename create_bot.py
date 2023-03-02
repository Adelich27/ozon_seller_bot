from aiogram import Bot
from aiogram.dispatcher import Dispatcher, storage
from tokens import botToken
from aiogram.contrib.fsm_storage.memory import MemoryStorage #хранение в оперативке


storage=MemoryStorage()
bot = Bot(token=botToken)
dp = Dispatcher(bot,storage=storage) 