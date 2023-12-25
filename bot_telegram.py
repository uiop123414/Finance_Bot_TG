from aiogram.utils import executor
from create_bot import dp
from data_base import postgresql_db
from handlers import client, admin, other


async def on_startup(_):
    print('Bot is online')
    postgresql_db.sql_start()


def start_bot():
    handlers = (client, admin, other)
    for handler in handlers:
        handler.register_handlers(dp)

    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
