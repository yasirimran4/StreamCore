from movie_app import App
import asyncio
from presentation import Presentation


class Main:
    def __init__(self, name="Netflix"):
        self.__app = App(name)

    async def start(self):
        print(f"Welcome to {self.__app.name}")
        presentation = Presentation()
        while True:
            choice = await presentation.authentication()  # Presentation Layer
            if choice == 1:
                await self.__app.register()
                break
            elif choice == 2:
                user = await self.__app.login()
                await self.__app.dashboard(user)
                break
            elif choice == 3:
                return
            else:
                print("Invalid Choice")


main = Main()
asyncio.run(main.start())
