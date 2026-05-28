# Decorator to check role of user if Logged In.
from functools import wraps


def is_admin(func):
    @wraps
    def wrapper(*args, **kwargs):
        user = args[1]
        if user.get_role() == "admin":
            return func(*args, **kwargs)

        print("User is not Admin")
        return None

    return wrapper
