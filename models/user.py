# User Class

class User:
    def __init__(self, username="", password="", role="user"):
        self.__username = username
        self.__password = password  # Private data members
        self.__role = role
        self.__login_status = False

    def set_login_status(self, status):  # After login change status
        self.__login_status = status

    # Getter Methods show encapsulation
    def get_login_status(self):
        return self.__login_status

    def get_role(self):
        return self.__role

    def get_username(self):
        return self.__username

    def get_password(self):
        return self.__password
