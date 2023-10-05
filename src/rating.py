class Rating:
    def __init__(self, stars: float, amount: int):
        self.stars = stars # rating out of 5 stars
        self.amount = amount # amount of ratings

    def __repr__(self):
        return f"{self.stars} stars with {self.amount} votes"