from decorators.admin_decorator import is_admin
from database.movie_data import MovieData
from decorators.auth_decorator import is_authenticated


# Movie Functions Class
class MovieService:
    def __init__(self, db):
        self.__data = MovieData(db)

    @is_admin
    async def add_movie(self, user, movie):
        try:
            await self.__data.add_movie(movie)
            return {"message": "Movie added successfully"}
        except Exception as e:
            print("Error :", e)

    @is_admin
    async def edit_movie(self, user, movie_id, new_title):
        try:
            await self.__data.edit_movie(new_title, movie_id)
            return {"message": "Movie edited successfully"}
        except Exception as e:
            print("Error :", e)

    @is_admin
    async def delete_movie(self, user, movie_id):
        try:
            await self.__data.delete_movie(movie_id)
            return {"message": "Movie deleted successfully"}
        except Exception as e:
            print("Error :", e)

    @is_authenticated
    async def like_movie(self, user, movie_id):
        try:
            await self.__data.like_movie(movie_id)
            return {"message": "Movie liked successfully"}
        except Exception as e:
            print("Error :", e)

    @is_authenticated
    async def watch_history(self, user):
        try:
            history = await self.__data.watch_history(user.get_id())
            if not history:
                return {"message": "History is Empty"}
            return history
        except Exception as e:
            print("Error :", e)

    @is_authenticated
    async def watch_movie(self, user, movie_id):  # watch movie on base of id
        try:
            movie = await self.__data.watch_movie(movie_id, user.get_id())
            if not movie:
                return {"message": "Movie not found."}
            return movie

        except Exception as e:
            print("Error :", e)

    @is_authenticated
    async def list_movies(self, user):
        try:
            movies = await self.__data.list_movies()
            if not movies:
                return {"message": "No Movies Exists"}
            return movies

        except Exception as e:
            print("Error :", e)
