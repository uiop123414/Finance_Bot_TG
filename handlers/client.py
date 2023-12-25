from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from keyboards import client_kb
from create_bot import bot
from aiogram.dispatcher.filters.state import State, StatesGroup
import finviz
from datetime import datetime
import sqlite3
from sec_funcs.sec_queries import get_report_url, download_file
import sqlite3


# from keyboards import kb_client
class Client:
    class FSMClient(StatesGroup):
        ticket = State()
        type = State()
        year = State()

    @staticmethod
    async def command_start(message: types.Message):
        sqlite_connection = sqlite3.Connection('sqlite_db')
        cursor = sqlite_connection.cursor()
        data = cursor.execute(f"SELECT COUNT(id) FROM users WHERE id={message.from_user.id}").fetchall()
        if data == [(0,)]:
            cursor.execute(f'INSERT INTO users (id,UserType,joining_date) VALUES (?, ?,?)',
                           (message.from_user.id, 1, datetime.now()))
            sqlite_connection.commit()
        elif data[0][0] == 0:
            await bot.send_message(message.from_user.id, text='Вы забанены!')
        sqlite_connection.close()
        await bot.send_message(message.from_user.id, 'В боте есть 2 основные функции.\n1. Отчет [Тикет Компании]'
                                                     ' (Например: Отчет AAPL).\n'
                                                     '2. Финансовые показатели [Тикет Компании] '
                                                     '(Например: Финансовые показатели AAPL).\n(Работают пока только '
                                                     'акции и только США)')

        await message.delete()

    # sec-api key 30d52e6e37ff6b4f07bcb15a3c62fcd4aa8be5b8bb5e142f4dcb79410934e4d5
    @staticmethod
    async def get_report(message: types.Message, state: FSMContext):
        await Client.FSMClient.ticket.set()
        sqlite_connection = sqlite3.Connection('sqlite_db')
        cursor = sqlite_connection.cursor()
        user_id = cursor.execute(f"SELECT UserType FROM users WHERE id= {message.from_user.id}").fetchall()[0][0]
        if user_id in (2, 3):
            async with state.proxy() as data:
                data['ticket'] = message.text.split()[1]
            await bot.send_message(message.from_user.id, text='Выбери тип отчета. Например 10-Q,10-K,8-K.')
            await Client.FSMClient.next()
        elif user_id == 0:
            await bot.send_message(message.from_user.id, text='Вы забанены!')
        else:
            await bot.send_message(message.from_user.id, text='Вы не можете получить отчет с SEC , потому что у вас '
                                                              'демо-аккаунт.')
        # await message.reply('Выбери тип отчета')



    @staticmethod
    async def load_type(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data['type'] = message.text
        await bot.send_message(message.from_user.id, text='Выбери год отчета.( Например 2022)')
        await Client.FSMClient.next()

    @staticmethod
    async def load_year(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data['year'] = message.text
        url = get_report_url(data['ticket'], data['year'], data['type'])
        await bot.send_message(message.from_user.id, text=url)
        await state.finish()

    @staticmethod
    async def get_properties(message: types.Message):
        sqlite_connection = sqlite3.Connection('sqlite_db')
        cursor = sqlite_connection.cursor()
        user_id = cursor.execute(f"SELECT UserType FROM users WHERE id = {message.from_user.id}").fetchall()[0][0]
        if user_id == 0:
            await bot.send_message(message.from_user.id, text='Вы забанены!')
        else:
            finance = finviz.get_stock(message.text.split()[2])
            text = str()
            for value in finance.items():
                text = text + f"{value[0]} : {value[1]} \n"
            await bot.send_message(message.from_user.id, text)


def register_handlers(dp: Dispatcher):
    commands = {'start': Client.command_start, 'help': Client.command_start, }
    for item in commands.items():
        dp.register_message_handler(item[1], commands=item[0])
    dp.register_message_handler(Client.get_report, (lambda x: x.text and x.text.startswith('Отчет ')))

    dp.register_message_handler(Client.load_type, state=Client.FSMClient.type)
    dp.register_message_handler(Client.load_year, state=Client.FSMClient.year)

    dp.register_message_handler(Client.get_properties,
                                (lambda x: x.text and x.text.startswith('Финансовые показатели ')))
