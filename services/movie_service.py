from decorators.admin_decorator import is_admin
from database.movie_data import MovieData


# Movie Functions Class
class MovieService:
    def __init__(self, db):
        self.__data = MovieData(db)

    @is_admin
    async def add_movie(self, movie):
        try:
            await self.__data.add_movie(movie)
            return {"message": "Movie added successfully"}
        except Exception as e:
            print("Error :", e)

    @is_admin
    async def edit_movie(self, new_movie, movie_id):
        try:
            await self.__data.edit_movie(new_movie, movie_id)
            return {"message": "Movie Edited successfully"}
        except Exception as e:
            print("Error :", e)

    @is_admin
    async def delete_movie(self, movie_id):
        try:
            await self.__data.delete_movie(movie_id)
            return {"message": "Movie deleted successfully"}
        except Exception as e:
            print("Error :", e)

    async def like_movie(self, likes, movie_id):
        try:
            await self.__data.like_movie(likes, movie_id)
            return {"message": "Movie liked successfully"}
        except Exception as e:
            print("Error :", e)

    async def watch_history(self, user_id):
        try:
            history = await self.__data.watch_history(user_id)
            if not history:
                return {"message": "History is Empty"}
            return history
        except Exception as e:
            print("Error :", e)

    async def watch_movie(self, movie_id, user_id):  # watch movie on base of id
        try:
            movie = await self.__data.watch_movie(movie_id, user_id)
            if not movie:
                return {"message": "Movie Watched successfully"}

        except Exception as e:
            print("Error :", e)

    async def list_movies(self):
        try:
            movies = await self.__data.list_movies()
            if not movies:
                return {"message": "No Movies Exists"}
            return movies

        except Exception as e:
            print("Error :", e)
