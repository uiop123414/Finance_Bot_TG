from bot_telegram import start_bot
import sqlite3


def main():
    try:
        sqlite_connection = sqlite3.Connection('sqlite_db')
        sqlite_create_table_query = """CREATE TABLE IF NOT EXISTS users 
                                    (id BIGINT PRIMARY KEY,
                                    UserType INTEGER,
                                    joining_date datetime,
                                    subscription_exp datetime)"""
        cursor = sqlite_connection.cursor()
        cursor.execute(sqlite_create_table_query)
    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")
    start_bot()


if __name__ == '__main__':
    main()
