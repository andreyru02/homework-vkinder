import sqlite3


class SQL:

    def __init__(self, database):
        """Подключение к БД"""
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()
        self.create_table_users()
        # self.create_table_photos()

    def create_table_users(self):
        """Создание таблицы для хранения юзеров"""
        with self.connection:
            return self.cursor.execute("CREATE TABLE IF NOT EXISTS users ('id' INTEGER NOT NULL UNIQUE, "
                                       "'user_id' INTEGER NOT NULL UNIQUE, "
                                       "'status' BOOLEAN DEFAULT FALSE,"
                                       "PRIMARY KEY ('id' AUTOINCREMENT ))")

    def create_table_photos(self):
        """Создание таблицы для хранения статуса фотографии"""
        with self.connection:
            return self.cursor.execute("CREATE TABLE IF NOT EXISTS photos ('id' INTEGER NOT NULL UNIQUE , "
                                       "'user_id' INTEGER NOT NULL , "
                                       "'url' TEXT, "
                                       "'status' BOOLEAN DEFAULT FALSE,"
                                       "PRIMARY KEY ('id' AUTOINCREMENT ),"
                                       "FOREIGN KEY ('user_id') REFERENCES 'users' ('user_id'))")

    def user_exists(self, user_id):
        """Проверяем, есть ли уже пользователь в базе"""
        with self.connection:
            result = self.cursor.execute('SELECT * FROM "users" WHERE "user_id" = ?', (user_id,)).fetchall()
            return bool(len(result))

    def add_user(self, user_id, status=False):
        """Добавляем нового пользователя"""
        with self.connection:
            return self.cursor.execute("INSERT INTO 'users' ('user_id', 'status') VALUES(?,?)", (user_id, status))

    def update_user(self, user_id, status):
        """Обновляем статус пользователя"""
        with self.connection:
            return self.cursor.execute("UPDATE 'users' SET 'status' = ? WHERE user_id = ?", (status, user_id))

    def get_user_favorites(self, user_id, status=True):
        """Ищем пользователя в избранных"""
        with self.connection:
            return bool(len(self.cursor.execute("SELECT status FROM 'users' WHERE (user_id, status) = (?,?)",
                                                (user_id, status)).fetchall()))

    def get_users_favorites(self, status=True):
        """Получаем всех пользователей из избранного"""
        with self.connection:
            return self.cursor.execute("SELECT user_id FROM 'users' WHERE status = ?", (status,)).fetchall()

    def close(self):
        """Закрываем соединение с БД"""
        self.connection.close()
