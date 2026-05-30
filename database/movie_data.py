# Class to interact with Movie Table in DB
class MovieData:
    def __init__(self, db):
        self.__db = db

    async def add_movie(self, movie):
        try:
            await self.__db.execute(
                "INSERT OR REPLACE INTO movies(title,likes,views) VALUES(?,?,?)",
                (
                    movie.get_title(),
                    movie.get_likes(),
                    movie.get_views(),
                ),
            )
            await self.__db.commit()
        except Exception as e:
            await self.__db.rollback()  # Rollback if any db error occurs
            print("DB error:", e)

    async def edit_movie(self, new_movie, movie_id):
        try:
            await self.__db.execute(
                "UPDATE movies SET title = ?, likes = ? , views = ? WHERE id = ?",
                (
                    new_movie.get_title(),
                    new_movie.get_likes(),
                    new_movie.get_views(),
                    movie_id,
                ),
            )
            await self.__db.commit()
        except Exception as e:
            await self.__db.rollback()
            print("DB error:", e)

    async def delete_movie(self, movie_id):
        try:
            await self.__db.execute("DELETE FROM movies WHERE id = ?", (movie_id,))
            await self.__db.commit()
        except Exception as e:
            await self.__db.rollback()
            print("DB error:", e)

    async def like_movie(self, likes, movie_id):
        try:
            await self.__db.execute(
                "UPDATE movies SET likes = ? WHERE id = ?", (likes, movie_id)
            )
        except Exception as e:
            await self.__db.rollback()
            print("DB error:", e)
            return None

    async def __views_increment(self, views, movie_id):
        try:
            await self.__db.execute(
                "UPDATE movies SET views = ? WHERE id = ?", (views, movie_id)
            )
        except Exception as e:
            await self.__db.rollback()
            print("DB error:", e)
            return None

    async def __store_history(self, user_id, movie_id):
        try:
            await self.__db.execute(
                "INSERT OR REPLACE INTO history (user_id,movie_id) ",
                (user_id, movie_id),  # Store Movies watched by this user
            )
            await self.__db.commit()
            print("History stored Successfully")
        except Exception as e:
            await self.__db.rollback()
            print("Invalid DB query: ", e)

    async def watch_history(self, user_id):
        try:
            result = await self.__db.execute(
                "SELECT * FROM history WHERE user_id = ?",
                (user_id),  # Movies watched by this user
            )
            return result.fetchall()
        except Exception as e:
            await self.__db.rollback()
            print("Invalid DB query: ", e)

    async def watch_movie(self, movie_id, user_id):  # watch movie on base of id
        try:
            movie = await self.__db.execute(
                "SELECT * FROM movies WHERE id = ?", (movie_id,)
            )
            await self.__views_increment(movie, id)  # On watch increment views
            await self.__store_history(user_id, movie_id)  # Store in History
            return movie.fetchone()
        except Exception as e:
            await self.__db.rollback()
            print("DB error:", e)
            return None

    async def list_movies(self):
        try:
            movies = await self.__db.execute("SELECT * FROM movies")
            return movies.fetchall()
        except Exception as e:
            await self.__db.rollback()
            print("DB error:", e)
            return None
