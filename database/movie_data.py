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

    async def edit_movie(self, new_title, movie_id):
        try:
            await self.__db.execute(
                "UPDATE movies SET title = ? WHERE id = ?",
                (new_title, movie_id),
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

    async def like_movie(self, movie_id):
        try:
            await self.__db.execute(
                "UPDATE movies SET likes = likes + 1 WHERE id = ?", (movie_id,)
            )
            await self.__db.commit()
        except Exception as e:
            await self.__db.rollback()
            print("DB error:", e)
            return None

    async def __views_increment(self, views, movie_id):
        try:
            await self.__db.execute(
                "UPDATE movies SET views = ? WHERE id = ?", (views, movie_id)
            )
            await self.__db.commit()
        except Exception as e:
            await self.__db.rollback()
            print("DB error:", e)
            return None

    async def __store_history(self, user_id, movie_id):
        try:
            await self.__db.execute(
                "INSERT OR REPLACE INTO history (user_id, movie_id) VALUES (?, ?)",
                (user_id, movie_id),  # Store Movies watched by this user
            )
            await self.__db.commit()
        except Exception as e:
            await self.__db.rollback()
            print("Invalid DB query: ", e)

    async def watch_history(self, user_id):
        try:
            result = await self.__db.execute(
                "SELECT history.id, history.movie_id, movies.title, history.watched_at "
                "FROM history JOIN movies ON history.movie_id = movies.id "
                "WHERE history.user_id = ?",
                (user_id,),
            )
            if not result:
                return None
            return await result.fetchall()
        except Exception as e:
            await self.__db.rollback()
            print("Invalid DB query: ", e)
            return None

    async def watch_movie(self, movie_id, user_id):  # watch movie on base of id
        try:
            cursor = await self.__db.execute(
                "SELECT * FROM movies WHERE id = ?", (movie_id,)
            )
            movie = await cursor.fetchone()
            if not movie:
                return None

            current_views = movie[3] if len(movie) > 3 and movie[3] is not None else 0
            await self.__views_increment(current_views + 1, movie_id)
            await self.__store_history(user_id, movie_id)
            return movie
        except Exception as e:
            await self.__db.rollback()
            print("DB error:", e)
            return None

    async def list_movies(self):
        try:
            movies = await self.__db.execute("SELECT * FROM movies")
            if not movies:
                return None
            return await movies.fetchall()
        except Exception as e:
            await self.__db.rollback()
            print("DB error:", e)
            return None
