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
            cursor.execute('''CREATE TABLE IF NOT EXISTS bot_users(
                            id SERIAL PRIMARY KEY,
                            username VARCHAR(50) NOT NULL,
                            user_initials VARCHAR(290),
                            chat_id	TEXT UNIQUE NOT NULL,
                            balance	INTEGER,
                            received_beats INTEGER,
                            received_free_options INTEGER,
                            beats_vers_messages TEXT DEFAULT '',
                            processing INTEGER DEFAULT 0,
                            beats_generating INTEGER DEFAULT 0);''')
            print('[INFO] Table "bot_users" works succesfuly') 

            cursor.execute('''CREATE TABLE IF NOT EXISTS orders(
                            id SERIAL PRIMARY KEY,
                            chat_id	TEXT UNIQUE NOT NULL,
                            chosen_style VARCHAR(50) DEFAULT NULL,
                            chosen_bpm VARCHAR(50) DEFAULT NULL,
                            chosen_extension VARCHAR(50) DEFAULT NULL,
                            chosen_harmony VARCHAR(50) DEFAULT NULL,
                            beats_ready INTEGER DEFAULT 0,
                            wait_for_file INTEGER DEFAULT 0
                            );''')
            print('[INFO] Table "orders" works succesfuly')

            cursor.execute('''CREATE TABLE IF NOT EXISTS query(
                            id SERIAL PRIMARY KEY,
                            chat_id	TEXT NOT NULL,
                            chosen_beat VARCHAR(50) DEFAULT NULL,
                            chosen_bpm VARCHAR(50) DEFAULT NULL,
                            chosen_format VARCHAR(50) DEFAULT NULL,
                            chosen_harmony VARCHAR(50) DEFAULT NULL,
                            order_number INTEGER
                            );''')
            print('[INFO] Table "query" works succesfuly')

            cursor.execute('''CREATE TABLE IF NOT EXISTS user_limits(
                            id SERIAL PRIMARY KEY,
                            chat_id TEXT UNIQUE NOT NULL,
                            free_options_use_limit INTEGER DEFAULT 0,
                            free_removes_use_limit INTEGER DEFAULT 0,
                            has_subscription BOOLEAN DEFAULT FALSE,
                            subscription_expiry_date DATE DEFAULT NULL,
                            last_updated DATE
                            );''')
            print('[INFO] Table "user_limits" works succesfuly')
            
        return True
    
    # запросы к таблице users
    def add_user(username, chat_id, user_initials='', balance=0):
        connect()
        with connection.cursor() as cursor:
            cursor.execute(f'''INSERT INTO bot_users (username, user_initials, chat_id, balance, received_beats, received_free_options)
            VALUES ('{username}', '{user_initials}', {chat_id}, {balance}, {0}, {0}) ON CONFLICT DO NOTHING;''')

            cursor.execute(f'''INSERT INTO orders (chat_id)
            VALUES ('{chat_id}') ON CONFLICT DO NOTHING;''')

            cursor.execute(f'''INSERT INTO user_limits (chat_id, free_options_use_limit, free_removes_use_limit, last_updated)
            VALUES ({chat_id}, {10}, {3}, NOW()) ON CONFLICT DO NOTHING;''')
            
            print(f'[INFO] Values for *{username}* succesfuly added')
    
    def get_user(chat_id):
        connect()
        with connection.cursor() as cursor:
            cursor.execute(f'''INSERT INTO orders (chat_id)
            VALUES ('{chat_id}') ON CONFLICT DO NOTHING;''')
            
            cursor.execute(f'''INSERT INTO user_limits (chat_id, free_options_use_limit, free_removes_use_limit, last_updated)
            VALUES ({chat_id}, {10}, {3}, NOW()) ON CONFLICT DO NOTHING;''')
            
            cursor.execute(f'''SELECT chat_id FROM bot_users WHERE CAST(chat_id AS BIGINT) = {chat_id};''')
            
            if cursor.fetchone() is None:
                return False
            else:
                return True
    
    def get_balance(chat_id):
        connect()
        with connection.cursor() as cursor:
            cursor.execute(f'''SELECT balance FROM bot_users WHERE CAST(chat_id AS BIGINT) = {chat_id};''')
            print(f'[INFO] The balance request for the *{chat_id}* was completed successfully')
            return cursor.fetchone()[0]
    def top_balance(chat_id, money):
        connect()
        with connection.cursor() as cursor:
            cursor.execute(f'''UPDATE bot_users SET balance = balance + {money} WHERE CAST(chat_id AS BIGINT) = {chat_id}''')
            print(f'[INFO] the balance of the *{chat_id}* has been successfully replenished')
    def pay(chat_id, payment):
        connect()
        with connection.cursor() as cursor:
            cursor.execute(f'''UPDATE bot_users SET balance = balance - {payment} WHERE CAST(chat_id AS BIGINT) = {chat_id}''')
            print(f'A fee of {payment} sizes has been withdrawn from the *{chat_id}* balance')
    
    def get_beat(chat_id):
        connect()
        with connection.cursor() as cursor:
            cursor.execute(f'''UPDATE bot_users SET received_beats = received_beats + 1 WHERE CAST(chat_id AS BIGINT) = {chat_id}''')
            print(f'[INFO] One received beat added to *{chat_id}* received beats')

    def get_free_option(chat_id):
        connect()
        with connection.cursor() as cursor:
            cursor.execute(f'''UPDATE bot_users SET received_free_options = received_free_options + 1 WHERE CAST(chat_id AS BIGINT) = {chat_id}''')
            print(f'[INFO] One free option added to *{chat_id}* received beats')

    def set_processing(chat_id):
        connect()
        with connection.cursor() as cursor:
            cursor.execute(f'''UPDATE bot_users SET processing = 1 WHERE CAST(chat_id AS BIGINT) = {chat_id}''')
            print(f'[INFO] *{chat_id}* in processing now')
    def del_processing(chat_id):
        connect()
        with connection.cursor() as cursor:
            cursor.execute(f'''UPDATE bot_users SET processing = 0 WHERE CAST(chat_id AS BIGINT) = {chat_id}''')
            print(f'[INFO] *{chat_id}* deleted from processing successfully')
    def get_processing(chat_id):
        connect()
        with connection.cursor() as cursor:
            cursor.execute(f'''SELECT processing FROM bot_users WHERE CAST(chat_id AS BIGINT) = {chat_id};''')
            print(f'[INFO] Getting processing for *{chat_id}* was completed successfully')
            return cursor.fetchone()[0]  
    def del_processing_for_all():
        connect()
        with connection.cursor() as cursor:
            cursor.execute(f'''UPDATE bot_users SET processing = 0''')
            print(f'[INFO] All deleted from processing successfully')   
    
    def set_beats_generating(chat_id):
        connect()
        with connection.cursor() as cursor:
            cursor.execute(f'''UPDATE bot_users SET beats_generating = 1 WHERE CAST(chat_id AS BIGINT) = {chat_id}''')
            print(f'[INFO] Setting beats_generating for *{chat_id}* was successfully')
    def del_beats_generating(chat_id):
        connect()
        with connection.cursor() as cursor:
            cursor.execute(f'''UPDATE bot_users SET beats_generating = 0 WHERE CAST(chat_id AS BIGINT) = {chat_id}''')
            print(f'[INFO] *{chat_id}* reset to 0 in beats_generating successfully') 
    def get_beats_generating(chat_id):
        connect()
        with connection.cursor() as cursor:
            cursor.execute(f'''SELECT beats_generating FROM bot_users WHERE CAST(chat_id AS BIGINT) = {chat_id};''')
            print(f'[INFO] Getting beats_generating for *{chat_id}* was completed successfully')
            return cursor.fetchone()[0]      
    
    def set_beats_versions_messages_ids(chat_id, messages_ids):
        connect()
        with connection.cursor() as cursor:
            cursor.execute(f'''UPDATE bot_users SET beats_vers_messages = '{messages_ids}' WHERE CAST(chat_id AS BIGINT) = {chat_id}''')
            print(f'[INFO] Setting beats_vers_messages for *{chat_id}* was completed successfully')
    def get_beats_versions_messages_ids(chat_id):
        connect()
        with connection.cursor() as cursor:
            cursor.execute(f'''SELECT beats_vers_messages FROM bot_users WHERE CAST(chat_id AS BIGINT) = {chat_id};''')
            print(f'[INFO] Getting beats_vers_messages was successfully')
            return cursor.fetchone()[0]      
    def del_beats_versions_messages_ids(chat_id):
        connect()
        with connection.cursor() as cursor:
            cursor.execute(f'''UPDATE bot_users SET beats_vers_messages = '' WHERE CAST(chat_id AS BIGINT) = {chat_id}''')
            print(f'[INFO] Deleting *{chat_id}* beats_vers_messages was successfully')

    def get_beats_generating_chat_ids():
        connect()
        with connection.cursor() as cursor:
            cursor.execute(f'''SELECT chat_id FROM bot_users WHERE CAST(beats_generating AS INTEGER) = 1;''')
            print(f'[INFO] Getting chat_ids by beats_generating was completed successfully')
            result = cursor.fetchall()
            return [row[0] for row in result]
    def get_chat_ids_by_messages_to_del_ids():
        connect()
        with connection.cursor() as cursor:
            cursor.execute(f'''SELECT chat_id FROM bot_users WHERE beats_vers_messages != '';''')
            print(f'[INFO] Getting chat_ids by messages_to_del_ids was completed successfully')
            result = cursor.fetchall()
            return [row[0] for row in result]

    # запросы к таблице orders
    def set_chosen_style(chat_id, user_chosen_style):
        connect()
        with connection.cursor() as cursor:
            cursor.execute(f'''UPDATE orders SET chosen_style = '{user_chosen_style}' WHERE CAST(chat_id AS BIGINT) = {chat_id}''')
            print(f'[INFO] Setting chosen_style for *{chat_id}* was successfully')
    def get_chosen_style(chat_id):
        connect()
        with connection.cursor() as cursor:
            cursor.execute(f'''SELECT chosen_style FROM orders WHERE CAST(chat_id AS BIGINT) = {chat_id};''')
            print(f'[INFO] Getting chosen_style was successfully')
            return cursor.fetchone()[0]   
    def del_chosen_style(chat_id):
        connect()
        with connection.cursor() as cursor:
            cursor.execute(f'''UPDATE orders SET chosen_style = '' WHERE CAST(chat_id AS BIGINT) = {chat_id}''')
            print(f'[INFO] Deleting *{chat_id}* chosen_style was successfully')
    
    def set_chosen_bpm(chat_id, user_chosen_bpm):
        connect()
        with connection.cursor() as cursor:
            cursor.execute(f'''UPDATE orders SET chosen_bpm = '{user_chosen_bpm}' WHERE CAST(chat_id AS BIGINT) = {chat_id}''')
            print(f'[INFO] Setting chosen_bpm for *{chat_id}* was successfully')
    def get_chosen_bpm(chat_id):
        connect()
        with connection.cursor() as cursor:
            cursor.execute(f'''SELECT chosen_bpm FROM orders WHERE CAST(chat_id AS BIGINT) = {chat_id};''')
            print(f'[INFO] Getting chosen_bpm was successfully')
            return cursor.fetchone()[0]   
    def del_chosen_bpm(chat_id):
        connect()
        with connection.cursor() as cursor:
            cursor.execute(f'''UPDATE orders SET chosen_bpm = '' WHERE CAST(chat_id AS BIGINT) = {chat_id}''')
            print(f'[INFO] Deleting *{chat_id}* chosen_bpm was successfully')

    def set_chosen_extension(chat_id, user_chosen_extension):
        connect()
        with connection.cursor() as cursor:
            cursor.execute(f'''UPDATE orders SET chosen_extension = '{user_chosen_extension}' WHERE CAST(chat_id AS BIGINT) = {chat_id}''')
            print(f'[INFO] Setting chosen_extension for *{chat_id}* was successfully')    
    def get_chosen_extension(chat_id):
        connect()
        with connection.cursor() as cursor:
            cursor.execute(f'''SELECT chosen_extension FROM orders WHERE CAST(chat_id AS BIGINT) = {chat_id};''')
            print(f'[INFO] Getting chosen_extension was successfully')
            return cursor.fetchone()[0]   
    def del_chosen_extension(chat_id):
        connect()
        with connection.cursor() as cursor:
            cursor.execute(f'''UPDATE orders SET chosen_extension = '' WHERE CAST(chat_id AS BIGINT) = {chat_id}''')
            print(f'[INFO] Deleting *{chat_id}* chosen_extension was successfully')

    def set_chosen_harmony(chat_id, user_chosen_harmony):
        connect()
        with connection.cursor() as cursor:
            cursor.execute(f'''UPDATE orders SET chosen_harmony = '{user_chosen_harmony}' WHERE CAST(chat_id AS BIGINT) = {chat_id}''')
            print(f'[INFO] Setting chosen_harmony for *{chat_id}* was successfully')    
    def get_chosen_harmony(chat_id):
        connect()
        with connection.cursor() as cursor:
            cursor.execute(f'''SELECT chosen_harmony FROM orders WHERE CAST(chat_id AS BIGINT) = {chat_id};''')
            print(f'[INFO] Getting chosen_harmony was successfully')
            return cursor.fetchone()[0]   
    def del_chosen_harmony(chat_id):
        connect()
        with connection.cursor() as cursor:
            cursor.execute(f'''UPDATE orders SET chosen_harmony = '' WHERE CAST(chat_id AS BIGINT) = {chat_id}''')
            print(f'[INFO] Deleting *{chat_id}* chosen_harmony was successfully')

    def set_beats_ready(chat_id):
        connect()
        with connection.cursor() as cursor:
            cursor.execute(f'''UPDATE orders SET beats_ready = 1 WHERE CAST(chat_id AS BIGINT) = {chat_id}''')
            print(f'[INFO] Setting beats_ready for *{chat_id}* was successfully')
    def del_beats_ready(chat_id):
        connect()
        with connection.cursor() as cursor:
            cursor.execute(f'''UPDATE orders SET beats_ready = 0 WHERE CAST(chat_id AS BIGINT) = {chat_id}''')
            print(f'[INFO] *{chat_id}* reset to 0 in beats_ready successfully') 
    def get_beats_ready(chat_id):
        connect()
        with connection.cursor() as cursor:
            cursor.execute(f'''SELECT beats_ready FROM orders WHERE CAST(chat_id AS BIGINT) = {chat_id};''')
            print(f'[INFO] Getting beats_ready for *{chat_id}* was completed successfully')
            return cursor.fetchone()[0]      
        
    def set_wait_for_file(chat_id):
        connect()
        with connection.cursor() as cursor:
            cursor.execute(f'''UPDATE orders SET wait_for_file = 1 WHERE CAST(chat_id AS BIGINT) = {chat_id}''')
            print(f'[INFO] Setting beats_ready for *{chat_id}* was successfully')
    def del_wait_for_file(chat_id):
        connect()
        with connection.cursor() as cursor:
            cursor.execute(f'''UPDATE orders SET wait_for_file = 0 WHERE CAST(chat_id AS BIGINT) = {chat_id}''')
            print(f'[INFO] *{chat_id}* reset to 0 in beats_ready successfully') 
    def get_wait_for_file(chat_id):
        connect()
        with connection.cursor() as cursor:
            cursor.execute(f'''SELECT wait_for_file FROM orders WHERE CAST(chat_id AS BIGINT) = {chat_id};''')
            print(f'[INFO] Getting beats_ready for *{chat_id}* was completed successfully')
            return cursor.fetchone()[0]     
    
    # запросы к таблице query
    def set_query(chat_id, chosen_beat, chosen_bpm, chosen_format, chosen_harmony):
        connect()
        with connection.cursor() as cursor:
            cursor.execute(f'''INSERT INTO query (chat_id, chosen_beat, chosen_bpm, chosen_format, chosen_harmony, order_number) VALUES ('{chat_id}', '{chosen_beat}', '{chosen_bpm}', '{chosen_harmony}', '{chosen_format}',  (SELECT COALESCE(MAX(order_number), 0) + 1 FROM query));''')
            print(f'[INFO] Query for {chat_id} added') 
    def get_query():
        connect()
        with connection.cursor() as cursor:
            cursor.execute(f'''SELECT chat_id, chosen_beat, chosen_bpm, chosen_format, chosen_harmony, order_number FROM query WHERE order_number = (SELECT MIN(order_number) FROM query);''')
            print(f'[INFO] Getting query')
            return cursor.fetchone()   
    def get_query_by_chat_id(chat_id):
        connect()
        with connection.cursor() as cursor:
            cursor.execute(f'''SELECT COUNT(*) AS position FROM query WHERE order_number <= (SELECT order_number FROM query WHERE CAST(chat_id AS BIGINT) = {chat_id});''')
            print(f'[INFO] Getting query for {chat_id}')
            return cursor.fetchone()[0] 
    def del_query():
        connect()
        with connection.cursor() as cursor:
            cursor.execute(f'''DELETE FROM query WHERE order_number = (SELECT MIN(order_number) FROM query);''')
            print(f'[INFO] Deleted query')
    def del_all_queries():
        connect()
        with connection.cursor() as cursor:
            cursor.execute(f'''DELETE FROM query;''')
            print(f'[INFO] Deleted all queries')
    def del_query_by_chat_id(chat_id):
        connect()
        with connection.cursor() as cursor:
            cursor.execute(f'''DELETE FROM query WHERE CAST(chat_id AS BIGINT) = {chat_id};''')
            print(f'[INFO] Deleted query for {chat_id}')

    # запросы к таблице user_limits
    def get_free_options_limit(chat_id):
        connect()
        with connection.cursor() as cursor:
            cursor.execute(f'''SELECT free_options_use_limit FROM user_limits WHERE CAST(chat_id AS BIGINT) = {chat_id}''')
            print(f'[INFO] Getting free_options_use_limit for *{chat_id}* was completed successfully')
            return cursor.fetchone()[0]        
    def draw_free_options_limit(chat_id):
        connect()
        with connection.cursor() as cursor:
            cursor.execute(f'''UPDATE user_limits SET free_options_use_limit = free_options_use_limit - 1 WHERE CAST(chat_id AS BIGINT) = {chat_id}''')
            print(f'[INFO] *{chat_id}* free_options_use_limit - 1')
    
    def get_removes_limit(chat_id):
        connect()
        with connection.cursor() as cursor:
            cursor.execute(f'''SELECT free_removes_use_limit FROM user_limits WHERE CAST(chat_id AS BIGINT) = {chat_id}''')
            print(f'[INFO] Getting free_removes_use_limit for *{chat_id}* was completed successfully')
            return cursor.fetchone()[0]   
    def draw_removes_limit(chat_id):
        connect()
        with connection.cursor() as cursor:
            cursor.execute(f'''UPDATE user_limits SET free_removes_use_limit = free_removes_use_limit - 1 WHERE CAST(chat_id AS BIGINT) = {chat_id}''')
            print(f'[INFO] *{chat_id}* free_removes_use_limit - 1')

    def refill_limits(chat_id):
        connect()
        with connection.cursor() as cursor:
            cursor.execute(f'''UPDATE user_limits SET free_removes_use_limit = 3, free_options_use_limit = 10, last_updated = NOW() WHERE CAST(chat_id AS BIGINT) = {chat_id}''')
            print(f'[INFO] *{chat_id}* limits refilled')

    def get_last_updated_limits(chat_id):
        connect()
        with connection.cursor() as cursor:
            cursor.execute(f'''SELECT last_updated FROM user_limits WHERE CAST(chat_id AS BIGINT) = {chat_id}''')
            print(f'[INFO] Getting last_updated_limits for *{chat_id}* was completed successfully')
            return cursor.fetchone()[0]

    def get_has_subscription(chat_id):
        connect()
        with connection.cursor() as cursor:
            cursor.execute(f'''SELECT has_subscription FROM user_limits WHERE CAST(chat_id AS BIGINT) = {chat_id}''')
            print(f'[INFO] Getting has_subscription for *{chat_id}* was completed successfully')
            return cursor.fetchone()[0]

except Exception as _ex:
    print('[INFO] Error while working with PostgreSQL', _ex)
finally:
    if connection:
        connection.close()
        print('[INFO] PostreSQL connection closed')
    