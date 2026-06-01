# Movie Class


class Movie:
    def __init__(self, name=""):  # Movie will be created by single admin of app
        self.__title = name
        self.__likes = 0
        self.__views = 0

    def get_title(self):
        return self.__title

    def get_likes(self):
        return self.__likes
        # Show Encapsulation

    def get_views(self):
        return self.__views

    def set_likes(self, likes):
        self.__likes = likes

    def set_views(self, views):
        self.__views = views
