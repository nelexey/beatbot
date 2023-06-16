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
                            user_initials VARCHAR(290),
                            chat_id	TEXT UNIQUE NOT NULL,
                            balance	INTEGER,
                            received_beats INTEGER,
                            beats_vers_messages TEXT DEFAULT '',
                            processing INTEGER DEFAULT 0,
                            chosen_style VARCHAR(50) DEFAULT NULL,
                            beats_generating INTEGER DEFAULT 0);''')
            print('[INFO] Table "users" works succesfuly')

            cursor.execute('''CREATE TABLE IF NOT EXISTS query(
                            id SERIAL PRIMARY KEY,
                            chat_id	TEXT NOT NULL,
                            chosen_beat VARCHAR(50) DEFAULT NULL,
                            chosen_bpm VARCHAR(50) DEFAULT NULL,
                            chosen_format VARCHAR(50) DEFAULT NULL,
                            order_number INTEGER
                            );''')
            print('[INFO] Table "query" works succesfuly')
            
        return True
    
    # запросы к таблице users
    def add_user(username, chat_id, user_initials='', balance=0):
        connect()
        with connection.cursor() as cursor:
            cursor.execute(f'''INSERT INTO users (username, user_initials, chat_id, balance, received_beats)
            VALUES ('{username}', '{user_initials}', {chat_id}, {balance}, {0}) ON CONFLICT DO NOTHING;''')
            
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
            print(f'[INFO] Getting processing for *{chat_id}* was completed successfully')
            return cursor.fetchone()[0]  
    def set_beats_generating(chat_id):
        connect()
        with connection.cursor() as cursor:
            cursor.execute(f'''UPDATE users SET beats_generating = 1 WHERE CAST(chat_id AS INTEGER) = {chat_id}''')
            print(f'[INFO] Setting beats_generating for *{chat_id}* was successfully')
    def del_beats_generating(chat_id):
        connect()
        with connection.cursor() as cursor:
            cursor.execute(f'''UPDATE users SET beats_generating = 0 WHERE CAST(chat_id AS INTEGER) = {chat_id}''')
            print(f'[INFO] *{chat_id}* reset to 0 in beats_generating successfully') 
    def get_beats_generating(chat_id):
        connect()
        with connection.cursor() as cursor:
            cursor.execute(f'''SELECT beats_generating FROM users WHERE CAST(chat_id AS INTEGER) = {chat_id};''')
            print(f'[INFO] Getting beats_generating for *{chat_id}* was completed successfully')
            return cursor.fetchone()[0]     
    def set_chosen_style(chat_id, user_chosen_style):
        connect()
        with connection.cursor() as cursor:
            cursor.execute(f'''UPDATE users SET chosen_style = '{user_chosen_style}' WHERE CAST(chat_id AS INTEGER) = {chat_id}''')
            print(f'[INFO] Setting chosen_style for *{chat_id}* was successfully')
    def del_chosen_style(chat_id):
        connect()
        with connection.cursor() as cursor:
            cursor.execute(f'''UPDATE users SET chosen_style = '' WHERE CAST(chat_id AS INTEGER) = {chat_id}''')
            print(f'[INFO] Deleting *{chat_id}* chosen_style was successfully')
    def get_chosen_style(chat_id):
        connect()
        with connection.cursor() as cursor:
            cursor.execute(f'''SELECT chosen_style FROM users WHERE CAST(chat_id AS INTEGER) = {chat_id};''')
            print(f'[INFO] Getting chosen_style was successfully')
            return cursor.fetchone()[0]   
    def del_chosen_style(chat_id):
        connect()
        with connection.cursor() as cursor:
            cursor.execute(f'''UPDATE users SET chosen_style = 0 WHERE CAST(chat_id AS INTEGER) = {chat_id}''')
            print(f'[INFO] Deleting *{chat_id}* chosen_style was successfully')

    def set_beats_versions_messages_ids(chat_id, messages_ids):
        connect()
        with connection.cursor() as cursor:
            cursor.execute(f'''UPDATE users SET beats_vers_messages = '{messages_ids}' WHERE CAST(chat_id AS INTEGER) = {chat_id}''')
            print(f'[INFO] Setting beats_vers_messages for *{chat_id}* was completed successfully')
    def get_beats_versions_messages_ids(chat_id):
        connect()
        with connection.cursor() as cursor:
            cursor.execute(f'''SELECT beats_vers_messages FROM users WHERE CAST(chat_id AS INTEGER) = {chat_id};''')
            print(f'[INFO] Getting beats_vers_messages was successfully')
            return cursor.fetchone()[0]      
    def del_beats_versions_messages_ids(chat_id):
        connect()
        with connection.cursor() as cursor:
            cursor.execute(f'''UPDATE users SET beats_vers_messages = '' WHERE CAST(chat_id AS INTEGER) = {chat_id}''')
            print(f'[INFO] Deleting *{chat_id}* beats_vers_messages was successfully')

    def get_beats_generating_chat_ids():
        connect()
        with connection.cursor() as cursor:
            cursor.execute(f'''SELECT chat_id FROM users WHERE CAST(beats_generating AS INTEGER) = 1;''')
            print(f'[INFO] Getting chat_ids by beats_generating was completed successfully')
            result = cursor.fetchall()
            return [row[0] for row in result]
    def get_chat_ids_by_messages_to_del_ids():
        connect()
        with connection.cursor() as cursor:
            cursor.execute(f'''SELECT chat_id FROM users WHERE beats_vers_messages != '';''')
            print(f'[INFO] Getting chat_ids by messages_to_del_ids was completed successfully')
            result = cursor.fetchall()
            return [row[0] for row in result]
        
    # запросы к таблице query
    def set_query(chat_id, chosen_beat, chosen_bpm, chosen_format):
        connect()
        with connection.cursor() as cursor:
            cursor.execute(f'''INSERT INTO query (chat_id, chosen_beat, chosen_bpm, chosen_format, order_number) VALUES ('{chat_id}', '{chosen_beat}', '{chosen_bpm}', '{chosen_format}',  (SELECT COALESCE(MAX(order_number), 0) + 1 FROM query));''')
            print(f'[INFO] Query for {chat_id} added')
    
    def get_query():
        connect()
        with connection.cursor() as cursor:
            cursor.execute(f'''SELECT chat_id, chosen_beat, chosen_bpm, chosen_format, order_number FROM query WHERE order_number = (SELECT MIN(order_number) FROM query);''')
            print(f'[INFO] Getting query')
            return cursor.fetchone() 
    
    def del_query():
        connect()
        with connection.cursor() as cursor:
            cursor.execute(f'''DELETE FROM query WHERE order_number = (SELECT MIN(order_number) FROM query);''')
            print(f'[INFO] Deleted query')
except Exception as _ex:
    print('[INFO] Error while working with PostgreSQL', _ex)
finally:
    if connection:
        connection.close()
        print('[INFO] PostreSQL connection closed')
        