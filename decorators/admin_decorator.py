# Decorator to check role of user if Logged In.

def is_admin(func):
    def wrapper(*args, **kwargs):
        user = args[1]
        if user.get_role() == "admin":
            return func(*args, **kwargs)

        print("User is not Admin")
        return None

    return wrapper
