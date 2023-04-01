import psycopg2
from config import host, user, password, db_name


try:
    connection = None
    def connect():
        global connection
        if connection != None: return False

        # подключение к БД
        connection = psycopg2.connect(host=host, 
                                    user=user, 
                                    password=password, 
                                    database=db_name,
                                    )

        connection.autocommit = True
    
        # создать таблицу users если её еще нет
        with connection.cursor() as cursor:
            cursor.execute('''CREATE TABLE IF NOT EXISTS users(
                            id SERIAL PRIMARY KEY,
                            username VARCHAR(50) NOT NULL,
                            chat_id	VARCHAR(50) UNIQUE NOT NULL,
                            balance	INTEGER,
                            received_beats INTEGER,
                            processing INTEGER DEFAULT 0);''')
            print('[INFO] Table works succesfuly')
        return True
    
    def add_user(username, chat_id, balance=0):
        connect()
        with connection.cursor() as cursor:
            cursor.execute(f'''INSERT INTO users (username, chat_id, balance, received_beats)
            VALUES ('{username}', {chat_id}, {balance}, {0}) ON CONFLICT DO NOTHING;''')
            
            print(f'[INFO] Values for *{username}* succesfuly added')
    def get_user(chat_id):
        connect()
        with connection.cursor() as cursor:
            cursor.execute(f'''SELECT chat_id FROM users WHERE CAST(chat_id AS INTEGER) = {chat_id};''')
            if cursor.fetchone() is None:
                return False
            else:
                return True
    def get_balance(chat_id):
        connect()
        with connection.cursor() as cursor:
            cursor.execute(f'''SELECT balance FROM users WHERE CAST(chat_id AS INTEGER) = {chat_id};''')
            print(f'[INFO] The balance request for the *{chat_id}* was completed successfully')
            return cursor.fetchone()[0]
    def top_balance(chat_id, money):
        connect()
        with connection.cursor() as cursor:
            cursor.execute(f'''UPDATE users SET balance = balance + {money} WHERE CAST(chat_id AS INTEGER) = {chat_id}''')
            print(f'[INFO] the balance of the *{chat_id}* has been successfully replenished')
    def pay(chat_id, payment):
        connect()
        with connection.cursor() as cursor:
            cursor.execute(f'''UPDATE users SET balance = balance - {payment} WHERE CAST(chat_id AS INTEGER) = {chat_id}''')
            print(f'A fee of {payment} sizes has been withdrawn from the *{chat_id}* balance')
    def get_beat(chat_id):
        connect()
        with connection.cursor() as cursor:
            cursor.execute(f'''UPDATE users SET received_beats = received_beats + 1 WHERE CAST(chat_id AS INTEGER) = {chat_id}''')
            print(f'[INFO] One received beat added to *{chat_id}* received beats')
    def set_processing(chat_id):
        connect()
        with connection.cursor() as cursor:
            cursor.execute(f'''UPDATE users SET processing = 1 WHERE CAST(chat_id AS INTEGER) = {chat_id}''')
            print(f'[INFO] *{chat_id}* in processing now')
    def del_processing(chat_id):
        connect()
        with connection.cursor() as cursor:
            cursor.execute(f'''UPDATE users SET processing = 0 WHERE CAST(chat_id AS INTEGER) = {chat_id}''')
            print(f'[INFO] *{chat_id}* deleted from processing successfully')
    def get_processing(chat_id):
        connect()
        with connection.cursor() as cursor:
            cursor.execute(f'''SELECT processing FROM users WHERE CAST(chat_id AS INTEGER) = {chat_id};''')
            print(f'[INFO] Get processing for *{chat_id}* was completed successfully')
            return cursor.fetchone()[0]
except Exception as _ex:
    print('[INFO] Error while working with PostgreSQL', _ex)
finally:
    if connection:
        connection.close()
        print('[INFO] PostreSQL connection closed')
        