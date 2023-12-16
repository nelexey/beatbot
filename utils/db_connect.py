import psycopg2
from psycopg2 import sql
from config.config import host, user, password, db_name


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
                            removes_ready INTEGER DEFAULT 0,
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

            cursor.execute('''CREATE TABLE IF NOT EXISTS options_query(
                            id SERIAL PRIMARY KEY,
                            chat_id TEXT UNIQUE NOT NULL,
                            chosen_format VARCHAR(50) DEFAULT NULL,
                            order_number INTEGER
                            );''')
            print('[INFO] Table "options_query" works succesfuly')

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

            cursor.execute('''CREATE TABLE IF NOT EXISTS logger(
                            id SERIAL PRIMARY KEY,
                            chat_id TEXT NOT NULL,
                            short_error TEXT DEFAULT NULL,
                            description TEXT DEFAULT NULL,
                            catched_at TIMESTAMP
                            );''')
            print('[INFO] Table "logger" works succesfuly')
            
        return True
    
    # запросы к таблице users
    def add_user(username, chat_id, user_initials='', balance=0):
        connect()
        with connection.cursor() as cursor:

            insert_user_query = sql.SQL('''
                INSERT INTO bot_users (username, user_initials, chat_id, balance, received_beats, received_free_options)
                VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING;
            ''')
            cursor.execute(insert_user_query, (username, user_initials, chat_id, balance, 0, 0))

            insert_orders_query = sql.SQL('''
                INSERT INTO orders (chat_id)
                VALUES (%s) ON CONFLICT DO NOTHING;
            ''')
            cursor.execute(insert_orders_query, (chat_id,))

            insert_user_limits_query = sql.SQL('''
                INSERT INTO user_limits (chat_id, free_options_use_limit, free_removes_use_limit, last_updated)
                VALUES (%s, %s, %s, NOW()) ON CONFLICT DO NOTHING;
            ''')
            cursor.execute(insert_user_limits_query, (chat_id, 10, 3))

        # print(f'[INFO] Values for *{username}* successfully added')
    
    # Запросы для получения пользователя
    def get_user(chat_id):
        connect()
        with connection.cursor() as cursor:

            insert_orders_query = sql.SQL('''
                INSERT INTO orders (chat_id)
                VALUES (%s) ON CONFLICT DO NOTHING;
            ''')
            cursor.execute(insert_orders_query, (chat_id,))

            insert_user_limits_query = sql.SQL('''
                INSERT INTO user_limits (chat_id, free_options_use_limit, free_removes_use_limit, last_updated)
                VALUES (%s, %s, %s, NOW()) ON CONFLICT DO NOTHING;
            ''')
            cursor.execute(insert_user_limits_query, (chat_id, 10, 3))

            select_user_query = sql.SQL('''
                SELECT chat_id FROM bot_users WHERE CAST(chat_id AS BIGINT) = %s;
            ''')
            cursor.execute(select_user_query, (chat_id,))

            if cursor.fetchone() is None:
                return False
            else:
                return True

    
    # Получение баланса
    def get_balance(chat_id):
        connect()
        with connection.cursor() as cursor:
            select_balance_query = sql.SQL('''
                SELECT balance FROM bot_users WHERE CAST(chat_id AS BIGINT) = %s;
            ''')
            cursor.execute(select_balance_query, (chat_id,))
            # print(f'[INFO] The balance request for the *{chat_id}* was completed successfully')
            return cursor.fetchone()[0]

    # Пополнение баланса
    def top_balance(chat_id, money):
        connect()
        with connection.cursor() as cursor:
            update_balance_query = sql.SQL('''
                UPDATE bot_users SET balance = balance + %s WHERE CAST(chat_id AS BIGINT) = %s;
            ''')
            cursor.execute(update_balance_query, (money, chat_id))
            # print(f'[INFO] the balance of the *{chat_id}* has been successfully replenished')

    # Списание с баланса
    def pay(chat_id, payment):
        connect()
        with connection.cursor() as cursor:
            update_balance_query = sql.SQL('''
                UPDATE bot_users SET balance = balance - %s WHERE CAST(chat_id AS BIGINT) = %s;
            ''')
            cursor.execute(update_balance_query, (payment, chat_id))
            # print(f'A fee of {payment} sizes has been withdrawn from the *{chat_id}* balance')

    # Увеличение счетчика полученных beats
    def get_beat(chat_id):
        connect()
        with connection.cursor() as cursor:
            update_beats_query = sql.SQL('''
                UPDATE bot_users SET received_beats = received_beats + 1 WHERE CAST(chat_id AS BIGINT) = %s;
            ''')
            cursor.execute(update_beats_query, (chat_id,))
            # print(f'[INFO] One received beat added to *{chat_id}* received beats')

    # Увеличение счетчика полученных бесплатных опций
    def get_free_option(chat_id):
        connect()
        with connection.cursor() as cursor:
            update_free_options_query = sql.SQL('''
                UPDATE bot_users SET received_free_options = received_free_options + 1 WHERE CAST(chat_id AS BIGINT) = %s;
            ''')
            cursor.execute(update_free_options_query, (chat_id,))
            # print(f'[INFO] One free option added to *{chat_id}* received beats')

    # Установка флага обработки для указанного пользователя
    def set_processing(chat_id):
        connect()
        with connection.cursor() as cursor:
            update_processing_query = sql.SQL('''
                UPDATE bot_users SET processing = 1 WHERE CAST(chat_id AS BIGINT) = %s;
            ''')
            cursor.execute(update_processing_query, (chat_id,))
            # print(f'[INFO] *{chat_id}* in processing now')

    # Удаление флага обработки для указанного пользователя
    def del_processing(chat_id):
        connect()
        with connection.cursor() as cursor:
            update_processing_query = sql.SQL('''
                UPDATE bot_users SET processing = 0 WHERE CAST(chat_id AS BIGINT) = %s;
            ''')
            cursor.execute(update_processing_query, (chat_id,))
            # print(f'[INFO] *{chat_id}* deleted from processing successfully')

    # Получение значения флага обработки для указанного пользователя
    def get_processing(chat_id):
        connect()
        with connection.cursor() as cursor:
            select_processing_query = sql.SQL('''
                SELECT processing FROM bot_users WHERE CAST(chat_id AS BIGINT) = %s;
            ''')
            cursor.execute(select_processing_query, (chat_id,))
            # print(f'[INFO] Getting processing for *{chat_id}* was completed successfully')
            return cursor.fetchone()[0]

    # Удаление флага обработки для всех пользователей
    def del_processing_for_all():
        connect()
        with connection.cursor() as cursor:
            update_all_processing_query = sql.SQL('''
                UPDATE bot_users SET processing = 0;
            ''')
            cursor.execute(update_all_processing_query)
            # print(f'[INFO] All deleted from processing successfully')

    
    # Установка флага генерации битов для указанного пользователя
    def set_beats_generating(chat_id):
        connect()
        with connection.cursor() as cursor:
            update_beats_generating_query = sql.SQL('''
                UPDATE bot_users SET beats_generating = 1 WHERE CAST(chat_id AS BIGINT) = %s;
            ''')
            cursor.execute(update_beats_generating_query, (chat_id,))
            # print(f'[INFO] Setting beats_generating for *{chat_id}* was successfully')

    # Сброс флага генерации битов для указанного пользователя
    def del_beats_generating(chat_id):
        connect()
        with connection.cursor() as cursor:
            update_beats_generating_query = sql.SQL('''
                UPDATE bot_users SET beats_generating = 0 WHERE CAST(chat_id AS BIGINT) = %s;
            ''')
            cursor.execute(update_beats_generating_query, (chat_id,))
            # print(f'[INFO] *{chat_id}* reset to 0 in beats_generating successfully')

    # Получение значения флага генерации битов для указанного пользователя
    def get_beats_generating(chat_id):
        connect()
        with connection.cursor() as cursor:
            select_beats_generating_query = sql.SQL('''
                SELECT beats_generating FROM bot_users WHERE CAST(chat_id AS BIGINT) = %s;
            ''')
            cursor.execute(select_beats_generating_query, (chat_id,))
            # print(f'[INFO] Getting beats_generating for *{chat_id}* was completed successfully')
            return cursor.fetchone()[0]
    
    # Установка сообщений версий битов для указанного пользователя
    def set_beats_versions_messages_ids(chat_id, messages_ids):
        connect()
        with connection.cursor() as cursor:
            update_beats_versions_messages_query = sql.SQL('''
                UPDATE bot_users SET beats_vers_messages = %s WHERE CAST(chat_id AS BIGINT) = %s;
            ''')
            cursor.execute(update_beats_versions_messages_query, (messages_ids, chat_id))
            # print(f'[INFO] Setting beats_vers_messages for *{chat_id}* was completed successfully')

    # Получение сообщений версий битов для указанного пользователя
    def get_beats_versions_messages_ids(chat_id):
        connect()
        with connection.cursor() as cursor:
            select_beats_versions_messages_query = sql.SQL('''
                SELECT beats_vers_messages FROM bot_users WHERE CAST(chat_id AS BIGINT) = %s;
            ''')
            cursor.execute(select_beats_versions_messages_query, (chat_id,))
            # print(f'[INFO] Getting beats_vers_messages was successfully')
            return cursor.fetchone()[0]

    # Удаление сообщений версий битов для указанного пользователя
    def del_beats_versions_messages_ids(chat_id):
        connect()
        with connection.cursor() as cursor:
            update_beats_versions_messages_query = sql.SQL('''
                UPDATE bot_users SET beats_vers_messages = '' WHERE CAST(chat_id AS BIGINT) = %s;
            ''')
            cursor.execute(update_beats_versions_messages_query, (chat_id,))
            # print(f'[INFO] Deleting *{chat_id}* beats_vers_messages was successfully')

    # Получение chat_ids пользователей, у которых идет генерация битов
    def get_beats_generating_chat_ids():
        connect()
        with connection.cursor() as cursor:
            select_chat_ids_query = sql.SQL('''
                SELECT chat_id FROM bot_users WHERE CAST(beats_generating AS INTEGER) = 1;
            ''')
            cursor.execute(select_chat_ids_query)
            # print(f'[INFO] Getting chat_ids by beats_generating was completed successfully')
            result = cursor.fetchall()
            return [row[0] for row in result]

    # Получение chat_ids пользователей, у которых есть сообщения для удаления
    def get_chat_ids_by_messages_to_del_ids():
        connect()
        with connection.cursor() as cursor:
            select_chat_ids_query = sql.SQL('''
                SELECT chat_id FROM bot_users WHERE beats_vers_messages != '';
            ''')
            cursor.execute(select_chat_ids_query)
            # print(f'[INFO] Getting chat_ids by messages_to_del_ids was completed successfully')
            result = cursor.fetchall()
            return [row[0] for row in result]

    # Получение всех chat_ids
    def get_all_chat_ids():
        connect()
        with connection.cursor() as cursor:
            select_chat_ids_query = sql.SQL('''
                SELECT chat_id FROM bot_users;
            ''')
            cursor.execute(select_chat_ids_query)
            # print(f'[INFO] Getting chat_ids was completed successfully')
            result = cursor.fetchall()
            return [row[0] for row in result]

    # запросы к таблице orders
    # Установка выбранного стиля для указанного пользователя
    def set_chosen_style(chat_id, user_chosen_style):
        connect()
        with connection.cursor() as cursor:
            update_chosen_style_query = sql.SQL('''
                UPDATE orders SET chosen_style = %s WHERE CAST(chat_id AS BIGINT) = %s;
            ''')
            cursor.execute(update_chosen_style_query, (user_chosen_style, chat_id))
            # print(f'[INFO] Setting chosen_style for *{chat_id}* was successfully')

    # Получение выбранного стиля для указанного пользователя
    def get_chosen_style(chat_id):
        connect()
        with connection.cursor() as cursor:
            select_chosen_style_query = sql.SQL('''
                SELECT chosen_style FROM orders WHERE CAST(chat_id AS BIGINT) = %s;
            ''')
            cursor.execute(select_chosen_style_query, (chat_id,))
            # print(f'[INFO] Getting chosen_style was successfully')
            return cursor.fetchone()[0]

    # Удаление выбранного стиля для указанного пользователя
    def del_chosen_style(chat_id):
        connect()
        with connection.cursor() as cursor:
            update_chosen_style_query = sql.SQL('''
                UPDATE orders SET chosen_style = '' WHERE CAST(chat_id AS BIGINT) = %s;
            ''')
            cursor.execute(update_chosen_style_query, (chat_id,))
            # print(f'[INFO] Deleting *{chat_id}* chosen_style was successfully')

    # Установка выбранного BPM для указанного пользователя
    def set_chosen_bpm(chat_id, user_chosen_bpm):
        connect()
        with connection.cursor() as cursor:
            update_chosen_bpm_query = sql.SQL('''
                UPDATE orders SET chosen_bpm = %s WHERE CAST(chat_id AS BIGINT) = %s;
            ''')
            cursor.execute(update_chosen_bpm_query, (user_chosen_bpm, chat_id))
            # print(f'[INFO] Setting chosen_bpm for *{chat_id}* was successfully')

    # Получение выбранного BPM для указанного пользователя
    def get_chosen_bpm(chat_id):
        connect()
        with connection.cursor() as cursor:
            select_chosen_bpm_query = sql.SQL('''
                SELECT chosen_bpm FROM orders WHERE CAST(chat_id AS BIGINT) = %s;
            ''')
            cursor.execute(select_chosen_bpm_query, (chat_id,))
            # print(f'[INFO] Getting chosen_bpm was successfully')
            return cursor.fetchone()[0]

    # Удаление выбранного BPM для указанного пользователя
    def del_chosen_bpm(chat_id):
        connect()
        with connection.cursor() as cursor:
            update_chosen_bpm_query = sql.SQL('''
                UPDATE orders SET chosen_bpm = '' WHERE CAST(chat_id AS BIGINT) = %s;
            ''')
            cursor.execute(update_chosen_bpm_query, (chat_id,))
            # print(f'[INFO] Deleting *{chat_id}* chosen_bpm was successfully')

    # Установка выбранного расширения для указанного пользователя
    def set_chosen_extension(chat_id, user_chosen_extension):
        connect()
        with connection.cursor() as cursor:
            update_chosen_extension_query = sql.SQL('''
                UPDATE orders SET chosen_extension = %s WHERE CAST(chat_id AS BIGINT) = %s;
            ''')
            cursor.execute(update_chosen_extension_query, (user_chosen_extension, chat_id))
            # print(f'[INFO] Setting chosen_extension for *{chat_id}* was successfully')

    # Получение выбранного расширения для указанного пользователя
    def get_chosen_extension(chat_id):
        connect()
        with connection.cursor() as cursor:
            select_chosen_extension_query = sql.SQL('''
                SELECT chosen_extension FROM orders WHERE CAST(chat_id AS BIGINT) = %s;
            ''')
            cursor.execute(select_chosen_extension_query, (chat_id,))
            # print(f'[INFO] Getting chosen_extension was successfully')
            return cursor.fetchone()[0]

    # Удаление выбранного расширения для указанного пользователя
    def del_chosen_extension(chat_id):
        connect()
        with connection.cursor() as cursor:
            update_chosen_extension_query = sql.SQL('''
                UPDATE orders SET chosen_extension = '' WHERE CAST(chat_id AS BIGINT) = %s;
            ''')
            cursor.execute(update_chosen_extension_query, (chat_id,))
            # print(f'[INFO] Deleting *{chat_id}* chosen_extension was successfully')

    # Установка выбранной гармонии для указанного пользователя
    def set_chosen_harmony(chat_id, user_chosen_harmony):
        connect()
        with connection.cursor() as cursor:
            update_chosen_harmony_query = sql.SQL('''
                UPDATE orders SET chosen_harmony = %s WHERE CAST(chat_id AS BIGINT) = %s;
            ''')
            cursor.execute(update_chosen_harmony_query, (user_chosen_harmony, chat_id))
            # print(f'[INFO] Setting chosen_harmony for *{chat_id}* was successfully')

    # Получение выбранной гармонии для указанного пользователя
    def get_chosen_harmony(chat_id):
        connect()
        with connection.cursor() as cursor:
            select_chosen_harmony_query = sql.SQL('''
                SELECT chosen_harmony FROM orders WHERE CAST(chat_id AS BIGINT) = %s;
            ''')
            cursor.execute(select_chosen_harmony_query, (chat_id,))
            # print(f'[INFO] Getting chosen_harmony was successfully')
            return cursor.fetchone()[0]

    # Удаление выбранной гармонии для указанного пользователя
    def del_chosen_harmony(chat_id):
        connect()
        with connection.cursor() as cursor:
            update_chosen_harmony_query = sql.SQL('''
                UPDATE orders SET chosen_harmony = '' WHERE CAST(chat_id AS BIGINT) = %s;
            ''')
            cursor.execute(update_chosen_harmony_query, (chat_id,))
            # print(f'[INFO] Deleting *{chat_id}* chosen_harmony was successfully')

    # Установка флага готовности битов для указанного пользователя
    def set_beats_ready(chat_id):
        connect()
        with connection.cursor() as cursor:
            update_beats_ready_query = sql.SQL('''
                UPDATE orders SET beats_ready = 1 WHERE CAST(chat_id AS BIGINT) = %s;
            ''')
            cursor.execute(update_beats_ready_query, (chat_id,))
            # print(f'[INFO] Setting beats_ready for *{chat_id}* was successfully')

    # Сброс флага готовности битов для указанного пользователя
    def del_beats_ready(chat_id):
        connect()
        with connection.cursor() as cursor:
            update_beats_ready_query = sql.SQL('''
                UPDATE orders SET beats_ready = 0 WHERE CAST(chat_id AS BIGINT) = %s;
            ''')
            cursor.execute(update_beats_ready_query, (chat_id,))
            # print(f'[INFO] *{chat_id}* reset to 0 in beats_ready successfully')

    # Получение значения флага готовности битов для указанного пользователя
    def get_beats_ready(chat_id):
        connect()
        with connection.cursor() as cursor:
            select_beats_ready_query = sql.SQL('''
                SELECT beats_ready FROM orders WHERE CAST(chat_id AS BIGINT) = %s;
            ''')
            cursor.execute(select_beats_ready_query, (chat_id,))
            # print(f'[INFO] Getting beats_ready for *{chat_id}* was completed successfully')
            return cursor.fetchone()[0]


    # Установка флага готовности удалений для указанного пользователя
    def set_removes_ready(chat_id, status=1):
        connect()
        with connection.cursor() as cursor:
            update_removes_ready_query = sql.SQL('''
                UPDATE orders SET removes_ready = %s WHERE CAST(chat_id AS BIGINT) = %s;
            ''')
            cursor.execute(update_removes_ready_query, (status, chat_id))
            # print(f'[INFO] Setting removes_ready for *{chat_id}* was successfully')

    # Сброс флага готовности удалений для указанного пользователя
    def del_removes_ready(chat_id):
        connect()
        with connection.cursor() as cursor:
            update_removes_ready_query = sql.SQL('''
                UPDATE orders SET removes_ready = 0 WHERE CAST(chat_id AS BIGINT) = %s;
            ''')
            cursor.execute(update_removes_ready_query, (chat_id,))
            # print(f'[INFO] *{chat_id}* reset to 0 in removes_ready successfully')

    # Получение значения флага готовности удалений для указанного пользователя
    def get_removes_ready(chat_id):
        connect()
        with connection.cursor() as cursor:
            select_removes_ready_query = sql.SQL('''
                SELECT removes_ready FROM orders WHERE CAST(chat_id AS BIGINT) = %s;
            ''')
            cursor.execute(select_removes_ready_query, (chat_id,))
            # print(f'[INFO] Getting removes_ready for *{chat_id}* was completed successfully')
            return cursor.fetchone()[0]
    
        
    # Установка флага ожидания файла для указанного пользователя
    def set_wait_for_file(chat_id):
        connect()
        with connection.cursor() as cursor:
            update_wait_for_file_query = sql.SQL('''
                UPDATE orders SET wait_for_file = 1 WHERE CAST(chat_id AS BIGINT) = %s;
            ''')
            cursor.execute(update_wait_for_file_query, (chat_id,))
            # print(f'[INFO] Setting wait_for_file for *{chat_id}* was successfully')

    # Сброс флага ожидания файла для указанного пользователя
    def del_wait_for_file(chat_id):
        connect()
        with connection.cursor() as cursor:
            update_wait_for_file_query = sql.SQL('''
                UPDATE orders SET wait_for_file = 0 WHERE CAST(chat_id AS BIGINT) = %s;
            ''')
            cursor.execute(update_wait_for_file_query, (chat_id,))
            # print(f'[INFO] *{chat_id}* reset to 0 in wait_for_file successfully')

    # Получение значения флага ожидания файла для указанного пользователя
    def get_wait_for_file(chat_id):
        connect()
        with connection.cursor() as cursor:
            select_wait_for_file_query = sql.SQL('''
                SELECT wait_for_file FROM orders WHERE CAST(chat_id AS BIGINT) = %s;
            ''')
            cursor.execute(select_wait_for_file_query, (chat_id,))
            # print(f'[INFO] Getting wait_for_file for *{chat_id}* was completed successfully')
            return cursor.fetchone()[0]
    
    
    # запросы к таблице query
    # Добавление запроса в таблицу query
    def set_query(chat_id, chosen_beat, chosen_bpm, chosen_format, chosen_harmony):
        connect()
        with connection.cursor() as cursor:
            insert_query_query = sql.SQL('''
                INSERT INTO query (chat_id, chosen_beat, chosen_bpm, chosen_format, chosen_harmony, order_number)
                VALUES (%s, %s, %s, %s, %s, (SELECT COALESCE(MAX(order_number), 0) + 1 FROM query));
            ''')
            cursor.execute(insert_query_query, (chat_id, chosen_beat, chosen_bpm, chosen_format, chosen_harmony))
            # print(f'[INFO] Query for {chat_id} added')

    # Получение первого запроса из таблицы query
    def get_query():
        connect()
        with connection.cursor() as cursor:
            select_query_query = sql.SQL('''
                SELECT chat_id, chosen_beat, chosen_bpm, chosen_format, chosen_harmony, order_number
                FROM query
                WHERE order_number = (SELECT MIN(order_number) FROM query);
            ''')
            cursor.execute(select_query_query)
            # print(f'[INFO] Getting query')
            return cursor.fetchone()

    # Получение порядкового номера запроса для указанного пользователя
    def get_query_by_chat_id(chat_id):
        connect()
        with connection.cursor() as cursor:
            select_query_by_chat_id_query = sql.SQL('''
                SELECT COUNT(*) AS position
                FROM query
                WHERE order_number <= (SELECT order_number FROM query WHERE CAST(chat_id AS BIGINT) = %s);
            ''')
            cursor.execute(select_query_by_chat_id_query, (chat_id,))
            # print(f'[INFO] Getting query for {chat_id}')
            return cursor.fetchone()[0]

    # Удаление первого запроса из таблицы query
    def del_query():
        connect()
        with connection.cursor() as cursor:
            delete_query_query = sql.SQL('''
                DELETE FROM query WHERE order_number = (SELECT MIN(order_number) FROM query);
            ''')
            cursor.execute(delete_query_query)
            # print(f'[INFO] Deleted query')

    # Удаление всех запросов из таблицы query
    def del_all_queries():
        connect()
        with connection.cursor() as cursor:
            delete_all_queries_query = sql.SQL('''
                DELETE FROM query;
            ''')
            cursor.execute(delete_all_queries_query)
            # print(f'[INFO] Deleted all queries')

    # Удаление запросов для указанного пользователя из таблицы query
    def del_query_by_chat_id(chat_id):
        connect()
        with connection.cursor() as cursor:
            delete_query_by_chat_id_query = sql.SQL('''
                DELETE FROM query WHERE CAST(chat_id AS BIGINT) = %s;
            ''')
            cursor.execute(delete_query_by_chat_id_query, (chat_id,))
            # print(f'[INFO] Deleted query for {chat_id}')

    # запросы к таблице options_query
    # Добавление запроса в таблицу options_query
    def set_options_query(chat_id, chosen_format):
        connect()
        with connection.cursor() as cursor:
            insert_options_query_query = sql.SQL('''
                INSERT INTO options_query (chat_id, chosen_format, order_number)
                VALUES (%s, %s, (SELECT COALESCE(MAX(order_number), 0) + 1 FROM options_query));
            ''')
            cursor.execute(insert_options_query_query, (chat_id, chosen_format))
            # print(f'[INFO] Options query for {chat_id} added')

    # Получение первого запроса из таблицы options_query
    def get_options_query():
        connect()
        with connection.cursor() as cursor:
            select_options_query_query = sql.SQL('''
                SELECT chat_id, chosen_format, order_number
                FROM options_query
                WHERE order_number = (SELECT MIN(order_number) FROM options_query);
            ''')
            cursor.execute(select_options_query_query)
            # print(f'[INFO] Getting options_query')
            return cursor.fetchone()

    # Получение порядкового номера запроса для указанного пользователя из таблицы options_query
    def get_options_query_by_chat_id(chat_id):
        connect()
        with connection.cursor() as cursor:
            select_options_query_by_chat_id_query = sql.SQL('''
                SELECT COUNT(*) AS position
                FROM options_query
                WHERE order_number <= (SELECT order_number FROM options_query WHERE CAST(chat_id AS BIGINT) = %s);
            ''')
            cursor.execute(select_options_query_by_chat_id_query, (chat_id,))
            # print(f'[INFO] Getting options_query for {chat_id}')
            return cursor.fetchone()[0]

    # Получение всех chat_id из таблицы options_query
    def get_options_query_chat_ids():
        connect()
        with connection.cursor() as cursor:
            select_options_query_chat_ids_query = sql.SQL('''
                SELECT chat_id FROM options_query;
            ''')
            cursor.execute(select_options_query_chat_ids_query)
            # print(f'[INFO] Getting all chat_ids from options_query')
            result = cursor.fetchall()
            return [row[0] for row in result]

    # Удаление первого запроса из таблицы options_query
    def del_options_query():
        connect()
        with connection.cursor() as cursor:
            delete_options_query_query = sql.SQL('''
                DELETE FROM options_query WHERE order_number = (SELECT MIN(order_number) FROM options_query);
            ''')
            cursor.execute(delete_options_query_query)
            # print(f'[INFO] Deleted first options_query')

    # Удаление всех запросов из таблицы options_query
    def del_all_options_queries():
        connect()
        with connection.cursor() as cursor:
            delete_all_options_queries_query = sql.SQL('''
                DELETE FROM options_query;
            ''')
            cursor.execute(delete_all_options_queries_query)
            # print(f'[INFO] Deleted all queries')

    # Удаление запросов для указанного пользователя из таблицы options_query
    def del_options_query_by_chat_id(chat_id):
        connect()
        with connection.cursor() as cursor:
            delete_options_query_by_chat_id_query = sql.SQL('''
                DELETE FROM options_query WHERE CAST(chat_id AS BIGINT) = %s;
            ''')
            cursor.execute(delete_options_query_by_chat_id_query, (chat_id,))
            # print(f'[INFO] Deleted options_query for {chat_id}')

    
    # запросы к таблице user_limits
    # Получение лимита на бесплатные опции
    def get_free_options_limit(chat_id):
        connect()
        with connection.cursor() as cursor:
            select_free_options_limit_query = sql.SQL('''
                SELECT free_options_use_limit
                FROM user_limits
                WHERE CAST(chat_id AS BIGINT) = %s;
            ''')
            cursor.execute(select_free_options_limit_query, (chat_id,))
            # print(f'[INFO] Getting free_options_use_limit for *{chat_id}* was completed successfully')
            return cursor.fetchone()[0]

    # Уменьшение лимита на бесплатные опции
    def draw_free_options_limit(chat_id):
        connect()
        with connection.cursor() as cursor:
            update_free_options_limit_query = sql.SQL('''
                UPDATE user_limits
                SET free_options_use_limit = free_options_use_limit - 1
                WHERE CAST(chat_id AS BIGINT) = %s;
            ''')
            cursor.execute(update_free_options_limit_query, (chat_id,))
            # print(f'[INFO] *{chat_id}* free_options_use_limit - 1')

    # Получение лимита на удаления
    def get_removes_limit(chat_id):
        connect()
        with connection.cursor() as cursor:
            select_removes_limit_query = sql.SQL('''
                SELECT free_removes_use_limit
                FROM user_limits
                WHERE CAST(chat_id AS BIGINT) = %s;
            ''')
            cursor.execute(select_removes_limit_query, (chat_id,))
            # print(f'[INFO] Getting free_removes_use_limit for *{chat_id}* was completed successfully')
            return cursor.fetchone()[0]

    # Уменьшение лимита на удаления
    def draw_removes_limit(chat_id):
        connect()
        with connection.cursor() as cursor:
            update_removes_limit_query = sql.SQL('''
                UPDATE user_limits
                SET free_removes_use_limit = free_removes_use_limit - 1
                WHERE CAST(chat_id AS BIGINT) = %s;
            ''')
            cursor.execute(update_removes_limit_query, (chat_id,))
            # print(f'[INFO] *{chat_id}* free_removes_use_limit - 1')

    # Пополнение лимитов пользователя
    def refill_limits(chat_id):
        connect()
        with connection.cursor() as cursor:
            refill_limits_query = sql.SQL('''
                UPDATE user_limits
                SET free_removes_use_limit = 3, free_options_use_limit = 10, last_updated = NOW()
                WHERE CAST(chat_id AS BIGINT) = %s;
            ''')
            cursor.execute(refill_limits_query, (chat_id,))
            # print(f'[INFO] *{chat_id}* limits refilled')

    # Получение времени последнего обновления лимитов пользователя
    def get_last_updated_limits(chat_id):
        connect()
        with connection.cursor() as cursor:
            select_last_updated_limits_query = sql.SQL('''
                SELECT last_updated
                FROM user_limits
                WHERE CAST(chat_id AS BIGINT) = %s;
            ''')
            cursor.execute(select_last_updated_limits_query, (chat_id,))
            # print(f'[INFO] Getting last_updated_limits for *{chat_id}* was completed successfully')
            return cursor.fetchone()[0]

    # Получение информации о наличии подписки у пользователя
    def get_has_subscription(chat_id):
        connect()
        with connection.cursor() as cursor:
            select_has_subscription_query = sql.SQL('''
                SELECT has_subscription
                FROM user_limits
                WHERE CAST(chat_id AS BIGINT) = %s;
            ''')
            cursor.execute(select_has_subscription_query, (chat_id,))
            # print(f'[INFO] Getting has_subscription for *{chat_id}* was completed successfully')
            return cursor.fetchone()[0]

    # Получение даты окончания подписки пользователя
    def get_subscription_expiry_date(chat_id):
        connect()
        with connection.cursor() as cursor:
            select_subscription_expiry_date_query = sql.SQL('''
                SELECT subscription_expiry_date
                FROM user_limits
                WHERE CAST(chat_id AS BIGINT) = %s;
            ''')
            cursor.execute(select_subscription_expiry_date_query, (chat_id,))
            # print(f'[INFO] Getting subscription_expiry_date for *{chat_id}* was completed successfully')
            return cursor.fetchone()[0]

    # Установка подписки для пользователя
    def set_subscription(chat_id, date):
        connect()
        with connection.cursor() as cursor:
            set_subscription_query = sql.SQL('''
                UPDATE user_limits
                SET free_removes_use_limit = 3, free_options_use_limit = 10, last_updated = NOW(), has_subscription=true, subscription_expiry_date = %s
                WHERE CAST(chat_id AS BIGINT) = %s;
            ''')
            cursor.execute(set_subscription_query, (date, chat_id))
            # print(f'[INFO] *{chat_id}* subscription updated')
    
    # Удаление подписки пользователя
    def del_subscription(chat_id):
        connect()
        with connection.cursor() as cursor:
            del_subscription_query = sql.SQL('''
                UPDATE user_limits
                SET has_subscription = false
                WHERE CAST(chat_id AS BIGINT) = %s;
            ''')
            cursor.execute(del_subscription_query, (chat_id,))
            # print(f'[INFO] *{chat_id}* subscription deleted')

    # Запись лога в таблицу logger
    def logger(chat_id, short_error, description):
        connect()
        # Используйте параметризованный запрос для избежания SQL-инъекций
        try:
            with connection.cursor() as cursor:
                logger_query = sql.SQL('''
                    INSERT INTO logger (chat_id, short_error, description, catched_at)
                    VALUES (%s, %s, %s, NOW());
                ''')
                cursor.execute(logger_query, (chat_id, short_error, description))
        except Exception as _ex:
            print('[INFO] Error while working with PostgreSQL', _ex)


except Exception as _ex:
    print('[INFO] Error while working with PostgreSQL', _ex)
finally:
    if connection:
        connection.close()
        print('[INFO] PostreSQL connection closed')
    