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

    def __init__(self, url: str, rating: Rating, time: int, author: str):
        self.url = url

        source = requests.get(self.url, headers=self.headers).text
        self.soup = BeautifulSoup(source, "lxml")

        self.title = self.soup.find("title").text
        self.author = author
        self.rating = rating
        self.time = time  # time in minutes
        self.ingredients = []
        self.servings = 0
        self.steps = []

        self.init_ingredients()
        self.init_servings()
        self.init_steps()

    def init_ingredients(self):
        # allrecipes.com, foodandwine.com
        if self.url.startswith(WebData.valid_sites[0]) or self.url.startswith(WebData.valid_sites[4]):
            ingredients_data = self.soup.find("ul", {"class": "mntl-structured-ingredients__list"}).find_all("li")
            for i in ingredients_data:
                self.ingredients.append(i.text.strip("\n").strip())
        # simplyrecipes.com
        if self.url.startswith(WebData.valid_sites[1]):
            ingredients_data = self.soup.find("ul", {"class": "structured-ingredients__list text-passage"}).find_all(
                "li")
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
        # print(self.ingredients)  # TODO for debugging, remove later

    def init_servings(self):
        # allrecipes.com
        if self.url.startswith(WebData.valid_sites[0]):
            servings_data = self.soup.find("div", {"class": "mntl-recipe-details__content"}).find_all(
                "div", {"class": "mntl-recipe-details__value"})[3].text
            self.servings = int(servings_data.split(" ")[0])

        # foodandwine.com
        if self.url.startswith(WebData.valid_sites[4]):
            servings_data = self.soup.find("div", {"class": "mntl-recipe-details__content"}).find_all(
                "div", {"class": "mntl-recipe-details__value"})[2].text
            self.servings = int(servings_data.split(" ")[0])

        # simplyrecipes.com
        if self.url.startswith(WebData.valid_sites[1]):
            servings_data = self.soup.find("div", {"class": "loc recipe-serving project-meta__recipe-serving"}).find(
                "span", {"class": "meta-text__data"}).text
            self.servings = int(servings_data.split(" ")[0])
        # foodnetwork.com
        if self.url.startswith(WebData.valid_sites[2]):
            servings_data = self.soup.find("ul", {"class": "o-RecipeInfo__m-Yield"}).find(
                "span", {"class": "o-RecipeInfo__a-Description"}).text
            self.servings = int(servings_data.split(" ")[0])
        # cooking.nytimes.com
        if self.url.startswith(WebData.valid_sites[3]):
            servings_data = self.soup.find("div", {"class": "ingredients_recipeYield__DN65p"}).find(
                "span", {"class": "pantry--ui ingredients_fontOverride__W_vGL"}).text
            self.servings = int(servings_data.split(" ")[0])
        # tasty.co
        if self.url.startswith(WebData.valid_sites[5]):
            servings_data = self.soup.find("div",
                                              {"class": "col md-col-4 xs-mx2 xs-pb3 md-mt0 xs-mt2"}).p.text
            self.servings = int(servings_data.split(" ")[1])
        # delish.com
        if self.url.startswith(WebData.valid_sites[6]):
            servings_data = self.soup.find("div", {"class": "css-1vkbd8k e1909yi85"}).find(
                "span", {"class": "css-nqfewg e1909yi82"}).text
            self.servings = int(servings_data.split(" ")[0])
        # justonecookbook.com, copykat.com
        if self.url.startswith(WebData.valid_sites[7]) or self.url.startswith(WebData.valid_sites[8]):
            servings_data = self.soup.select("span.wprm-recipe-servings")[0].text
            self.servings = int(servings_data.split(" ")[0])
        # seriouseats.com
        if self.url.startswith(WebData.valid_sites[9]):
            servings_data = self.soup.find("div", {"class": "loc recipe-serving project-meta__recipe-serving"}).find(
                "span", {"class": "meta-text__data"}).text
            self.servings = int(servings_data.split(" ")[0])
        # print(self.servings)  # TODO for debugging, remove later

    def init_steps(self):
        # allrecipes.com, foodandwine.com
        if self.url.startswith(WebData.valid_sites[0]) or self.url.startswith(WebData.valid_sites[4]):
            steps_data = self.soup.find("div", {"class": "comp recipe__steps-content mntl-sc-page mntl-block"}).find_all("li")
            for s in steps_data:
                self.steps.append(s.p.text.strip("\n").strip())
        # simplyrecipes.com
        if self.url.startswith(WebData.valid_sites[1]):
            steps_data = self.soup.find("div", {"class": "comp text-passage structured-content structured-project__steps mntl-sc-page mntl-block"}).find_all(
                "li")
            for s in steps_data:
                self.steps.append(s.p.text.strip("\n").strip())
        # foodnetwork.com
        if self.url.startswith(WebData.valid_sites[2]):
            steps_data = self.soup.find("div",
                                              {"class": "o-Method__m-Body"}).find_all(
                "li", {"class": "o-Method__m-Step"})
            for s in steps_data:
                self.steps.append(s.text.strip())
        # cooking.nytimes.com
        if self.url.startswith(WebData.valid_sites[3]):
            steps_data = self.soup.find("ol",
                                              {"class": "preparation_stepList___jqWa"}).find_all(
                "li")
            for s in steps_data:
                self.steps.append(s.p.text.strip())
        # tasty.co
        if self.url.startswith(WebData.valid_sites[5]):
            steps_data = self.soup.find("ol",
                                        {"class": "prep-steps list-unstyled xs-text-3"}).find_all(
                "li")
            for s in steps_data:
                self.steps.append(s.text.strip())
        # delish.com
        if self.url.startswith(WebData.valid_sites[6]):
            steps_data = self.soup.find("ol",
                                        {"class": "css-19p7hma et3p2gv0"}).find_all(
                "li")
            for s in steps_data:
                s = s.find("span", {"class": "css-13o7eu2 eagam8p1"})
                self.steps.append(s.text.strip())
        # justonecookbook.com
        if self.url.startswith(WebData.valid_sites[7]):
            steps_data = self.soup.find("div",
                                        {"class": "wprm-recipe-instructions-container wprm-recipe-59223-instructions-container wprm-block-text-normal"}).find_all(
                "li")
            for s in steps_data:
                self.steps.append(s.span.text.strip())
        # copykat.com
        if self.url.startswith(WebData.valid_sites[8]):
            steps_data = self.soup.find_all("ol")
            steps_data.pop()
            for s in steps_data:
                self.steps += [step.text for step in s.find_all("li")]
        # seriouseats.com
        if self.url.startswith(WebData.valid_sites[9]):
            steps_data = self.soup.find("ol",
                                        {"class": "comp mntl-sc-block-group--OL mntl-sc-block mntl-sc-block-startgroup"}).find_all(
                "li")
            for s in steps_data:
                self.steps.append(s.p.text.strip())
        # print(self.steps)  # TODO for debugging, remove later

    def __repr__(self):
        return (f"URL: {self.url} \n Title: {self.title} \n Author: {self.author} \n Rating: {repr(self.rating)} \n Time: {self.time} mins")