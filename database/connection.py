import aiosqlite  # For Db connection


class DBConnection:
    def __init__(self, file_path) -> None:
        self.__file_path = file_path
        self.__db = None

    async def initialize_db(self):
        self.__db = await aiosqlite.connect(self.__file_path)
        await self.__db.execute("PRAGMA foreign_keys = ON;")  # By default Foreign Key is disables in sqlite
        print("DB initialized Successfully")

    def get_db(self):
        return self.__db

    async def close_db(self):
        assert self.__db is not None  # Tell Pylance that db will not be None
        await self.__db.close()
        print("DB connection Closed")
