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
                                    database=db_name)

        connection.autocommit = True
    
        # создать таблицу users если её еще нет
        with connection.cursor() as cursor:
            cursor.execute('''CREATE TABLE IF NOT EXISTS users(
                            id SERIAL PRIMARY KEY,
                            username VARCHAR(50) NOT NULL,
                            chat_id	VARCHAR(50) UNIQUE NOT NULL,
                            balance	INTEGER);''')
            print('[INFO] Table works succesfuly')
        return True
    
    def add_user(username, chat_id, balance=0):
        connect()
        with connection.cursor() as cursor:
            cursor.execute(f'''INSERT INTO users (username, chat_id, balance)
            VALUES ('{username}', {chat_id}, {balance}) ON CONFLICT DO NOTHING;''')
            
            print(f'[INFO] Values for *{username}* succesfuly added')
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
            print(f'[INFO] The balance of the *{chat_id}* has been successfully replenished')
    def pay(chat_id, payment):
        connect()
        with connection.cursor() as cursor:
            cursor.execute(f'''UPDATE users SET balance = balance - {payment} WHERE CAST(chat_id AS INTEGER) = {chat_id}''')
            print(f'[INFO] A fee of {payment} sizes has been withdrawn from the *{chat_id}* balance')
   
except Exception as _ex:
    print('[INFO] Error while working with PostgreSQL', _ex)
finally:
    if connection:
        connection.close()
        print('[INFO] PostreSQL connection closed')
        