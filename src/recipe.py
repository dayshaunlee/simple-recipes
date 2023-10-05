# A recipe with a URL, name, portion size, ingredients, and steps
from src.rating import Rating


class Recipe:
    def __init__(self, url: str, rating: Rating, time):
        self.url = url
        self.title = "temp"
        self.rating = rating
        self.time = time
        self.ingredients = []
        self.steps = ""
        # TODO properly initialize attributes

    def __repr__(self):
        return (f"URL: {self.url} \n Rating: {repr(self.rating)} \n Time: {self.time}")
