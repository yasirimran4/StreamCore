from database.user_data import UserData


# Auth Class handles register,login etc
class Auth:
    def __init__(self, db) -> None:
        self.__data = UserData(db)

    async def register_user(self, user):
        try:
            result = await self.__data.find_user(user.get_username())
            if result is not None:
                return {"message": "User already Registered with this username"}

            await self.__data.store_user(user)  # Store user in db and send sattus code
            return {"message": "User Registered Successfully"}
        except Exception as e:
            print("Error ", e)

    async def login_user(self, user):
        try:
            result = await self.__data.find_user(user.get_username())
            if result is None:
                return {"message": "User does not exists with this username"}
            elif user.get_password() != result[2]:
                return {"message": "Password is wrong. Try Again"}
            elif user.get_role() != result[3]:
                return {"message": "User does not exists with this role"}
            else:
                user.set_login_status(True)
                user.set_id(result[0])
                return {"message": "User Logged in Successfully"}
        except Exception as e:
            print("Error ", e)
