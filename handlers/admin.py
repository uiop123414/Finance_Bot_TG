import sqlite3
from datetime import datetime

from create_bot import bot
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


class Admin:
    class FSMAdmin(StatesGroup):
        user_id = State()
        type = State()

    @staticmethod
    async def change_user_type(message: types.Message, state: FSMContext):
        sqlite_connection = sqlite3.Connection('sqlite_db')
        cursor = sqlite_connection.cursor()
        user_id = cursor.execute(f"SELECT UserType FROM users WHERE id= {message.from_user.id}").fetchall()[0][0]
        if user_id == 3:
            await bot.send_message(message.from_user.id, text='Id пользователя!')
            await Admin.FSMAdmin.next()
        else:
            await bot.send_message(message.from_user.id, text='Вы не можете менять статус пользователей!')
            cursor.close()
    @staticmethod
    async def load_id(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data['user_id'] = message.text
        await Admin.FSMAdmin.next()
        await bot.send_message(message.from_user.id, text='Тип нового пользователя.\n0-Забаненный.\n1'
                                                          '-Демо-пользователь.\n2-Про-пользователь.\n'
                                                          '3-Администратор.')

    @staticmethod
    async def get_user_type(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data['type'] = float(message.text)
        sqlite_connection = sqlite3.Connection('sqlite_db')
        cursor = sqlite_connection.cursor()
        if not cursor.execute(f"SELECT UserType FROM users WHERE id = {data['user_id']}").fetchall():
            cursor.execute(f'INSERT INTO users (id,UserType,joining_date) VALUES (?, ?,?)',
                           (data['user_id'], data['type'], datetime.now()))
        else:
            cursor.execute(f'Update users set UserType = {data["type"]} where id = {data["user_id"]}')
        sqlite_connection.commit()
        sqlite_connection.close()
        await state.finish()  #


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(Admin.change_user_type, commands='user_change')
    dp.register_message_handler(Admin.load_id, state=Admin.FSMAdmin.user_id)
    dp.register_message_handler(Admin.get_user_type, state=Admin.FSMAdmin.type)

