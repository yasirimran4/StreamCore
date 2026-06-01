# Class for making Tables in DB


class Schema:
    def __init__(self, db):
        self.__db = db  # DB alive connection

        # Create User Table

    async def __create_user_table(self):
        try:
            await self.__db.execute(""" CREATE TABLE IF NOT EXISTS users 
                (id INTEGER PRIMARY KEY, username TEXT UNIQUE,
                password TEXT, role TEXT, created_at DATETIME
                DEFAULT CURRENT_TIMESTAMP)""")
        except Exception as e:
            await self.__db.rollback()
            print("DB error:", e)
            return None    
        print("User Table created Successfully")

        # Create Movie table

    async def __create_movie_table(self):
        try:
            await self.__db.execute(""" CREATE TABLE IF NOT EXISTS movies 
                (id INTEGER PRIMARY KEY, title TEXT,
                likes INTEGER, views INTEGER, created_at DATETIME
                DEFAULT CURRENT_TIMESTAMP)""")
        except Exception as e:
            await self.__db.rollback()
            print("DB error:", e)
            return None    
        print("Movie Table created Successfully")

    async def __create_history_table(self):
        try:
            await self.__db.execute(""" CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            movie_id INTEGER NOT NULL,
            watched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(user_id, movie_id),
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (movie_id) REFERENCES movies(id) ) """)
        except Exception as e:
            await self.__db.rollback()
            print("DB error:", e)
            return None

        print("History Table created Successfully")

    async def create_all_tables(self):
        try:
            await self.__create_user_table()
            await self.__create_movie_table()
            await self.__create_history_table()

            await self.__db.commit()  # Commit all changes to db
            print("All Tables created Successfully")
        except Exception as e:
            await self.__db.rollback()
            print("DB error:", e)
            return None    
