import asyncio
from database.connection import DBConnection
from database.schema import Schema
from services.auth_service import Auth
from services.movie_service import MovieService
from models.user import User
from models.movie import Movie


async def prompt(text: str) -> str:
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, input, text)


def show_menu(user):
    print("\n=== Movie App CLI ===")
    if user is not None:
        print(f"Logged in as: {user.get_username()} with this role : ({user.get_role()})")
    else:
        print("Not logged in")
    print("1. Register")
    print("2. Login")
    print("3. List movies")
    print("4. Add movie (admin)")
    print("5. Edit movie (admin)")
    print("6. Delete movie (admin)")
    print("7. Like movie")
    print("8. Watch movie")
    print("9. View watch history")
    print("10. Logout")
    print("0. Exit")


def print_movies(movies):
    if not movies:
        print("No movies available.")
        return

    print("\nMovies:")
    print("ID | Title | Likes | Views | Created At")
    print("----------------------------------------")
    for movie in movies:
        if movie is None:
            continue
        print(
            f"{movie[0]} | {movie[1]} | {movie[2]} | {movie[3]} | {movie[4] if len(movie) > 4 else ''}"
        )


def print_history(history):
    if not history:
        print("No watch history found.")
        return

    print("\nWatch History:")
    print("ID | Movie ID | Movie Title")
    print("-------------------------")
    for record in history:
        print(f"{record[0]} | {record[1]} | {record[2]}")


async def register_user(auth_service):
    username = (await prompt("Username: ")).strip()
    password = (await prompt("Password: ")).strip()
    role = (await prompt("Role (admin/user): ")).strip().lower()
    if role not in ["admin", "user"]:
        print("Invalid role. So Using 'user'.")
        role = "user"

    user = User(username, password, role)
    result = await auth_service.register_user(user)
    if result is not None:
        print(result.get("message"))


async def login_user(auth_service):
    username = (await prompt("Username: ")).strip()
    password = (await prompt("Password: ")).strip()
    role = (await prompt("Role (admin/user): ")).strip().lower()
    if role not in ["admin", "user"]:
        print("Invalid role. Defaulting to 'user'.")
        role = "user"

    user = User(username, password, role)
    result = await auth_service.login_user(user)
    print(result.get("message"))

    if "Logged" in result.get("message", ""):
        return user
    return None


async def main_menu():
    db_connection = DBConnection("storage/movie_app.db")
    await db_connection.initialize_db()
    db = db_connection.get_db()

    schema = Schema(db)
    await schema.create_all_tables()

    auth_service = Auth(db)
    movie_service = MovieService(db)

    current_user = None
    try:
        while True:
            show_menu(current_user)
            choice = (await prompt("Choose an option: ")).strip()

            if choice == "1":
                await register_user(auth_service)
            elif choice == "2":
                current_user = await login_user(auth_service)
            elif choice == "3":
                if current_user is None or not current_user.get_login_status():
                    print("Please login first to view movies.")
                else:
                    movies = await movie_service.list_movies(current_user)
                    if isinstance(movies, dict):
                        print(movies.get("message"))
                    else:
                        print_movies(movies)
            elif choice == "4":
                if current_user is None:
                    print("Please login as admin to add movies.")
                else:
                    title = (await prompt("Movie title: ")).strip()
                    movie = Movie(title)
                    result = await movie_service.add_movie(current_user, movie)
                    if result is not None:
                        print(result.get("message"))
            elif choice == "5":
                if current_user is None:
                    print("Please login as admin to edit movies.")
                else:
                    movies = await movie_service.list_movies(current_user)
                    print_movies(movies)
                    movie_id = (await prompt("Movie ID to edit: ")).strip()
                    title = (await prompt("New title: ")).strip()
                    try:
                        movie_id = int(movie_id)
                    except ValueError:
                        print("Invalid movie ID.")
                        continue
                    result = await movie_service.edit_movie(
                        current_user, movie_id, title
                    )
                    if result is not None:
                        print(result.get("message"))
            elif choice == "6":
                if current_user is None:
                    print("Please login as admin to delete movies.")
                else:
                    movie_id = (await prompt("Movie ID to delete: ")).strip()
                    try:
                        movie_id = int(movie_id)
                    except ValueError:
                        print("Invalid movie ID.")
                        continue
                    result = await movie_service.delete_movie(current_user, movie_id)
                    if result is not None:
                        print(result.get("message"))
            elif choice == "7":
                if current_user is None or not current_user.get_login_status():
                    print("Please login first to like movies.")
                else:
                    movie_id = (await prompt("Movie ID to like: ")).strip()
                    try:
                        movie_id = int(movie_id)
                    except ValueError:
                        print("Invalid movie ID.")
                        continue
                    result = await movie_service.like_movie(current_user, movie_id)
                    if result is not None:
                        print(result.get("message"))
            elif choice == "8":
                if current_user is None or not current_user.get_login_status():
                    print("Please login first to watch movies.")
                else:
                    movie_id = (await prompt("Movie ID to watch: ")).strip()
                    try:
                        movie_id = int(movie_id)
                    except ValueError:
                        print("Invalid movie ID.")
                        continue
                    result = await movie_service.watch_movie(current_user, movie_id)
                    if isinstance(result, dict):
                        print(result.get("message"))
                    else:
                        if result is None:
                            print("Movie not found.")
                        else:
                            print(f"You watched: {result[1]}")
            elif choice == "9":
                if current_user is None or not current_user.get_login_status():
                    print("Please login first to view history.")
                else:
                    history = await movie_service.watch_history(current_user)
                    if isinstance(history, dict):
                        print(history.get("message"))
                    else:
                        print_history(history)
            elif choice == "10":
                if current_user is not None:
                    current_user.set_login_status(False)
                    current_user = None
                    print("Logged out successfully.")
                else:
                    print("You are not logged in.")
            elif choice == "0":
                print("Exiting application.")
                break
            else:
                print("Invalid option, please choose again.")
    finally:
        await db_connection.close_db()


def run_cli():
    asyncio.run(main_menu())


if __name__ == "__main__":
    run_cli()
