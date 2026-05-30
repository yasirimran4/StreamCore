# Class to interact with User Table in DB

class UserData:
    def __init__(self, db):
        self.__db = db

    async def find_user(self, username):
        result = await self.__db.execute(
            "SELECT * FROM users WHERE username = ?", (username,)
        )
        return await result.fetchone()  # Convert to Row

    async def store_user(self, user):
        await self.__db.execute(
            "INSERT INTO users(username,password,role) VALUES(?,?,?)",
            (
                user.get_username(),
                user.get_password(),
                user.get_role(),
            ),
        )
        await self.__db.commit()
