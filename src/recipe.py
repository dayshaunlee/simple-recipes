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

        # allrecipes.com, foodandwine.com
        if self.url.startswith(WebData.valid_sites[0]) or self.url.startswith(WebData.valid_sites[4]):
            ingredients_data = self.soup.find("ul", {"class": "mntl-structured-ingredients__list"}).find_all("li")
            for i in ingredients_data:
                self.ingredients.append(i.text.strip("\n").strip())

        # simplyrecipes.com
        if self.url.startswith(WebData.valid_sites[1]):
            ingredients_data = self.soup.find("ul", {"class": "structured-ingredients__list text-passage"}).find_all("li")
            for i in ingredients_data:
                self.ingredients.append(i.text.strip("\n").strip())

        # foodnetwork.com
        if self.url.startswith(WebData.valid_sites[2]):
            ingredients_data = self.soup.find("div",
                                              {"class": "o-Ingredients__m-Body"}).find_all(
                "p", {"class": "o-Ingredients__a-Ingredient"})
            for i in ingredients_data:
                if i.text.strip() != "Deselect All":
                    self.ingredients.append(i.text.strip())

        # cooking.nytimes.com
        if self.url.startswith(WebData.valid_sites[3]):
            ingredients_data = self.soup.find("div",
                                              {"class": "ingredients_ingredients__FLjsC"}).find_all(
                "li")
            for i in ingredients_data:
                if i.text[0].isalpha() is False:
                    self.ingredients.append((i.text[0] + " " + i.text[1:]).strip("\n").strip())
                else:
                    self.ingredients.append(i.text.strip("\n").strip())

        # tasty.co
        if self.url.startswith(WebData.valid_sites[5]):
            ingredients_data = self.soup.find("div",
                                              {"class": "col md-col-4 xs-mx2 xs-pb3 md-mt0 xs-mt2"}).find_all(
                "li")
            for i in ingredients_data:
                self.ingredients.append(i.text.strip("\n").strip())

        # delish.com
        if self.url.startswith(WebData.valid_sites[6]):
            ingredients_data = self.soup.find("div",
                                              {"class": "ingredients-body css-0 eno1xhi5"}).find_all(
                "li")
            for i in ingredients_data:
                # ignore nutritional information
                if i.parent.parent["class"][-1] != "e11kntxf5":
                    self.ingredients.append(i.text.strip("\n").strip())

        # justonecookbook.com, copykat.com
        if self.url.startswith(WebData.valid_sites[7]) or self.url.startswith(WebData.valid_sites[8]):
            ingredients_data = self.soup.find_all(
                "li", {"class": "wprm-recipe-ingredient"})
            for i in ingredients_data:
                self.ingredients.append(i.text.strip("\n").strip("▢").strip())

        # seriouseats.com
        if self.url.startswith(WebData.valid_sites[9]):
            ingredients_data = self.soup.find_all(
                "li", {"class": "structured-ingredients__list-item"})
            for i in ingredients_data:
                self.ingredients.append(i.text.strip("\n").strip().replace("\xa0", " "))

        print(self.ingredients) # TODO for debugging, remove later

    def __repr__(self):
        return (f"URL: {self.url} \n Title: {self.title} \n Rating: {repr(self.rating)} \n Time: {self.time} mins")
