from bs4 import BeautifulSoup
import requests

from src.rating import Rating

# A recipe with a URL, name, portion size, ingredients, and steps
class Recipe:
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/117.0.0.0 Safari/537.36"
    }
    def __init__(self, url: str, rating: Rating, time: int):
        self.url = url

        source = requests.get(self.url, headers=self.headers).text
        self.soup = BeautifulSoup(source, "lxml")

        self.title = self.soup.find("title").text
        self.rating = rating
        self.time = time # time in minutes
        self.ingredients = []
        self.steps = ""
        # TODO properly initialize attributes
        # TODO make search and recipe extend some soup class

    def __repr__(self):
        return (f"URL: {self.url} \n Title: {self.title} \n Rating: {repr(self.rating)} \n Time: {self.time} mins")
