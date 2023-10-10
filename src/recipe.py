from bs4 import BeautifulSoup
import requests

from src.rating import Rating
from src.webdata import WebData


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
        self.time = time  # time in minutes
        self.ingredients = []
        self.steps = ""

        # allrecipes.com
        if self.url.startswith(WebData.valid_sites[0]):
            ingredients_data = self.soup.find("ul", {"class": "mntl-structured-ingredients__list"}).find_all("li")
            for i in ingredients_data:
                self.ingredients.append(i.text.strip("\n").strip())

        # simplyrecipes.com
        if self.url.startswith(WebData.valid_sites[1]):
            ingredients_data = self.soup.find("ul", {"class": "structured-ingredients__list text-passage"}).find_all("li")
            for i in ingredients_data:
                self.ingredients.append(i.text.strip("\n").strip())

        print(self.ingredients)
        # TODO properly initialize attributes
        # TODO make search and recipe extend some soup class

    def __repr__(self):
        return (f"URL: {self.url} \n Title: {self.title} \n Rating: {repr(self.rating)} \n Time: {self.time} mins")
