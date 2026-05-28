# Decorator to check status of user if Logged In.
from functools import wraps


def is_authenticated(func):
    @wraps
    def wrapper(*args, **kwargs):
        user = args[1]

        if user.get_login_status() == True:
            return func(*args, **kwargs)

        print("User is not Authenticated")
        return None

    return wrapper
