import customtkinter as ctk

from src.recipe import Recipe
from src.search import Search


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("600x500")
        self.title("Noodle")

        self.current_page = None
        self.select_page("home")

    def select_page(self, page):
        # TODO remove elements first

        if page == "home":
            self.to_home()
        if page == "search":
            self.to_search()
        if page == "recipe":
            self.to_recipe()

    def to_home(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.current_page = HomePage(self)
        self.current_page.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="ew")

    def to_search(self, query):
        for item in self.current_page.winfo_children():
            item.destroy()
        self.current_page.destroy()
        self.current_page = SearchPage(self)
        self.current_page.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="ew")
        self.search(query)

    def to_recipe(self):
        pass

    def search(self, query):
        self.current_page.entry.insert(0, query)
        search = Search(query)
        search.search()
        if self.current_page.frame is not None:
            for item in self.current_page.frame.winfo_children():
                item.destroy()
            self.current_page.frame.destroy()
        self.current_page.fill([search.results[recipe] for recipe in search.results])


class HomePage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.label = ctk.CTkLabel(self, width=375, height=150, text="Noodle", text_color="#FCE4B1",
                                  font=("Product Sans", 100))
        self.label.grid(row=0, column=0, padx=10, pady=10)

        self.entry = ctk.CTkEntry(self, width=580, height=50, corner_radius=30, font=("Arial", 12))
        self.entry.grid(row=1, column=0, padx=(5, 8), pady=(0, 14))

        self.button = ctk.CTkButton(self, width=200, height=35, text="Noodle Search", fg_color="#303134",
                                    hover_color="#404144", command=lambda: master.to_search(self.entry.get()))
        self.button.grid(row=2, column=0, pady=16)


class SearchPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.frame = None
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_columnconfigure(2, weight=1)

        self.label = ctk.CTkLabel(self, width=150, height=30, text="Noodle", text_color="#FCE4B1",
                                  font=("Product Sans", 20))
        self.label.grid(row=0, column=0, padx=(5, 25), pady=(0, 10))
        # TODO add a button on this to go back to home page

        self.entry = ctk.CTkEntry(self, width=580, height=50, corner_radius=30, font=("Arial", 12))
        self.entry.grid(row=0, column=1, padx=(5, 8), pady=(10, 14), sticky="ew")

        self.button = ctk.CTkButton(self, width=150, height=20, text="Search", fg_color="#303134",
                                    hover_color="#404144", font=("Product Sans", 15),
                                    command=lambda: master.search(self.entry.get()))
        self.button.grid(row=0, column=2, padx=(10, 5), pady=(0, 14))

    def fill(self, recipes):
        n = 0
        for r in recipes:
            self.grid_rowconfigure(n+1, weight=1)
            self.frame = SearchResult(self, r)
            self.frame.grid(row=n+1, column=0, columnspan=2, padx=5, pady=10, sticky="ew")
            n += 1


class SearchResult(ctk.CTkFrame):
    def __init__(self, master, recipe: Recipe):
        super().__init__(master)
        self.grid_rowconfigure(0, weight=1)  # author
        self.grid_rowconfigure(1, weight=1)  # title
        self.grid_rowconfigure(2, weight=1)  # rating/time

        # author label
        self.label = ctk.CTkLabel(self, width=200, height=20, text=recipe.author, text_color="white",
                                  font=("Arial", 10))
        self.label.grid(row=0, column=0)

        # title label
        self.label = ctk.CTkLabel(self, height=31, text=recipe.title, text_color="#8AB4F8",
                                  font=("Arial", 12))
        self.label.grid(row=1, column=0)
        # TODO bind this to a button

        # rating/time label
        hours = recipe.time // 60
        minutes = recipe.time - 60*hours
        if hours == 0:
            time_str = f"{str(minutes)} mins"
        else:
            time_str = f"{str(hours)}h {str(minutes)}mins"
        self.label = ctk.CTkLabel(self, width=200, height=20, text=f"Rating: {str(recipe.rating)}, Time: {time_str}", text_color="white",
                                  font=("Arial", 10))
        self.label.grid(row=2, column=0)


app = App()
app.mainloop()
