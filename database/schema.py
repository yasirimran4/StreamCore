# Class for making Tables in DB


class Schema:
    def __init__(self, db):
        self.__db = db  # DB alive connection

        # Create User Table

    async def __create_user_table(self):

        await self.__db.execute(""" CREATE TABLE IF NOT EXISTS users 
            (id INTEGER PRIMARY KEY, username TEXT UNIQUE,
            password TEXT, role TEXT, created_at DATETIME
             DEFAULT CURRENT_TIMESTAMP)""")
        print("User Table created Successfully")

        # Create Movie table

    async def __create_movie_table(self):

        await self.__db.execute(""" CREATE TABLE IF NOT EXISTS movies 
            (id INTEGER PRIMARY KEY, title TEXT,
            likes INTEGER, views INTEGER, created_at DATETIME
             DEFAULT CURRENT_TIMESTAMP)""")
        print("Movie Table created Successfully")

    async def __create_history_table(self):
        await self.__db.execute(""" CREATE TABLE IF NOT EXISTS history 
            (id INTEGER PRIMARY KEY, user_id INTEGER, 
            movie_id INTEGER, FOREIGN KEY (user_id) 
            REFERENCES users(id) , FOREIGN KEY (movie_id) 
            REFERENCES movies(id) """)

        print("History Table created Successfully")

    async def create_all_tables(self):
        await self.__create_user_table()
        await self.__create_movie_table()
        await self.__create_history_table()

        await self.__db.commit()  # Commit all changes to db
        print("All Tables created Successfully")
