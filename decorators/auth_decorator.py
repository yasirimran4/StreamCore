# Decorator to check status of user if Logged In.

def is_authenticated(func):
    def wrapper(*args, **kwargs):
        user = args[1]

        if user.get_login_status() == True:
            return func(*args, **kwargs)

        print("User is not Authenticated")
        return None

    return wrapper
