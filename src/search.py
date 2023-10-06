from bs4 import BeautifulSoup
import requests

from src.rating import Rating
from src.recipe import Recipe


# A search query with results that are recipes
class Search:
    SEARCH_STRING = "https://www.google.com/search?hl=en&q="

    # user-agent so Google doesn't block the search
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/117.0.0.0 Safari/537.36"
    }

    def __init__(self, query):
        self.query = query
        self.url = self.SEARCH_STRING + "+".join(self.query.split(" "))
        self.results = {}  # URL -> Recipe

        source = requests.get(self.url, headers=self.headers).text
        self.soup = BeautifulSoup(source, "lxml")

        with open("./valid_websites.txt", 'r') as f:
            self.valid_sites = [x for x in f.read().strip().splitlines()]

        # print(self.soup.prettify())

    def search(self):
        sites = self.soup.select("div.g")
        for site in sites:
            url = site.a["href"]
            rating_data = site.find("div", class_="smukrd")
            # check if the site is a recipe website and has a star-rating
            if any(map(lambda s: url.startswith(s), self.valid_sites)) and rating_data is not None:
                # parse rating data and create a rating
                rating_data = rating_data.text
                score = float(rating_data.split(" · ")[0].split(": ")[-1])
                votes = int(rating_data.split(" · ")[1].split(" ")[0].replace(",", ""))
                rating = Rating(score, votes)

                # parse time data (in the same line as rating data) and convert to numerical time
                time_data = rating_data.split(" · ")[2].rpartition("hrs ")
                if time_data[0].isdigit():
                    hrs = int(time_data[0])
                else:
                    hrs = 0
                mins = int(time_data[-1].split(" ")[0])
                time = hrs * 60 + mins

                self.results[url] = Recipe(url, rating, time)
        print(self.results)
