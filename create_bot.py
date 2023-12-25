import json

from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()

token = json.load(open('data.json', 'r'))['token']

bot = Bot(token=token)
dp = Dispatcher(bot, storage=storage)
