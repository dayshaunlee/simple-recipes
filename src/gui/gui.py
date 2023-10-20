import customtkinter as ctk

from src.recipe import Recipe
from src.search import Search


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("700x600")
        self.title("Noodle")

        self.current_page = None
        self.select_page("home")

    def select_page(self, page):
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

    def to_recipe(self, recipe: Recipe):
        for item in self.current_page.winfo_children():
            item.destroy()
        self.current_page.destroy()
        self.current_page = RecipePage(self, recipe)
        self.current_page.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="ew")

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

        self.entry = ctk.CTkEntry(self, width=580, height=50, corner_radius=30, font=("Arial", 12))
        self.entry.grid(row=0, column=1, padx=(5, 8), pady=(10, 14), sticky="ew")

        self.button = ctk.CTkButton(self, width=150, height=20, text="Search", fg_color="#303134",
                                    hover_color="#404144", font=("Product Sans", 15),
                                    command=lambda: master.search(self.entry.get()))
        self.button.grid(row=0, column=2, padx=(10, 5), pady=(0, 14))

    def fill(self, recipes):
        n = 0
        for r in recipes:
            self.grid_rowconfigure(n + 1, weight=1)
            self.frame = SearchResult(self, r)
            self.frame.grid(row=n + 1, column=0, columnspan=2, padx=5, pady=10, sticky="ew")
            n += 1


class SearchResult(ctk.CTkFrame):
    def __init__(self, master, recipe: Recipe):
        super().__init__(master)
        self.recipe = recipe

        self.grid_rowconfigure(0, weight=1)  # author
        self.grid_rowconfigure(1, weight=1)  # title
        self.grid_rowconfigure(2, weight=1)  # rating/time

        # author label
        self.label = ctk.CTkLabel(self, width=200, height=20, text=self.recipe.author, text_color="white",
                                  font=("Arial", 10))
        self.label.grid(row=0, column=0, sticky="w")

        # title label
        self.label = ctk.CTkLabel(self, height=31, text=self.recipe.title, text_color="#8AB4F8",
                                  font=("Arial", 12))
        self.label.grid(row=1, column=0, sticky="w")
        self.label.bind("<Button-1>", command=lambda e: master.master.to_recipe(self.recipe))
        # TODO bind this to a button

        # rating/time label
        hours = recipe.time // 60
        minutes = recipe.time - 60 * hours
        if hours == 0:
            time_str = f"{str(minutes)} mins"
        else:
            time_str = f"{str(hours)}h {str(minutes)}mins"
        self.label = ctk.CTkLabel(self, width=200, height=20, text=f"Rating: {str(recipe.rating)}, Time: {time_str}",
                                  text_color="white",
                                  font=("Arial", 10))
        self.label.grid(row=2, column=0, sticky="w")


class RecipePage(ctk.CTkFrame):
    def __init__(self, master, recipe: Recipe):
        super().__init__(master)
        self.n_ings = 0
        self.n_steps = 0
        self.ing_font_size = 10
        self.ste_font_size = 10

        self.grid_rowconfigure(0, weight=3)  # titles: recipe name and steps
        self.grid_rowconfigure(1, weight=1)  # time                {      }
        self.grid_rowconfigure(2, weight=1)  # servings            { step }
        self.grid_rowconfigure(3, weight=2)  # ingredients title   { list }
        self.grid_rowconfigure(4, weight=3)  # ingredient list     {      }

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)  # step title and step list

        # recipe title
        self.title = ctk.CTkLabel(self, text=recipe.title, height=50, font=("Arial", 20), justify="center")
        self.title.label.configure(wraplength=200)
        self.title.grid(row=0, column=0, padx=15, pady=(5, 10))
        hours = recipe.time // 60
        minutes = recipe.time - 60 * hours
        if hours == 0:
            time_str = f"{str(minutes)} mins"
        else:
            time_str = f"{str(hours)}h {str(minutes)}mins"
        self.time = ctk.CTkLabel(self, height=30, text=f"Time: {time_str}",
                                 font=("Arial", 10))
        self.time.grid(row=1, column=0, padx=(15, 0), sticky="w")
        # rating label
        self.rating = ctk.CTkLabel(self, height=30, text=f"Rating: {str(recipe.rating)}",
                                   font=("Arial", 10))
        self.rating.grid(row=2, column=0, padx=10, sticky="w")

        # ingredients title
        self.ingredients_title = ctk.CTkLabel(self, text="Ingredients", width=150,
                                              font=("Arial", 15), justify="left")
        self.ingredients_title.grid(row=3, column=0, padx=10)
        # ingredients
        self.ingredients = ctk.CTkFrame(self)
        self.ingredients.grid_columnconfigure(0, weight=1)
        # ingredient
        ingredient = []
        for n, i in enumerate(recipe.ingredients):
            self.n_ings += 1
            self.ingredients.grid_rowconfigure(n, weight=1)
            ingredient.append(ctk.CTkCheckBox(self.ingredients, width=100, text=i, font=("Arial", self.ing_font_size)))
            ingredient[n].grid(row=n, column=0, padx=15, pady=10, sticky="w")
        self.ingredients.grid(row=4, column=0, padx=10, pady=(0, 20), sticky="ew")

        # steps title
        self.steps_title = ctk.CTkLabel(self, text="Steps", font=("Arial", 25))
        self.steps_title.grid(row=0, column=1, rowspan=2, padx=15, pady=(5, 20), sticky="s")
        # steps
        self.steps = ctk.CTkFrame(self)
        self.steps.grid_columnconfigure(0, weight=1)  # steps

        step = []
        for n, s in enumerate(recipe.steps):
            self.n_steps += 1
            self.steps.grid_rowconfigure(n, weight=1)
            step.append(ctk.CTkLabel(self.steps, width=200, text=f"{n + 1}.  {s}", font=("Arial", self.ste_font_size), justify="left"))
            step[n].grid(row=n, column=0, padx=15, pady=5, sticky="nw")
        self.steps.grid(row=1, column=1, rowspan=self.n_ings - 1, padx=10, pady=20, sticky="nesw")

        self.title.bind("<Configure>", lambda e: wrap())

        def wrap():
            self.title.label.configure(
                wraplength=self.ingredients.winfo_width() - 20)
            for ing in ingredient:
                ing.text_label.configure(wraplength=self.ingredients.winfo_width() * 3 / 5 - 10)
                if self.ing_font_size >= 5 and self.ste_font_size <= 20:
                    font_size = 20 - 2 * self.n_ings
                    if font_size < 5:
                        font_size = 10
                    ing.configure(font=("Arial", font_size))
            for ste in step:
                ste.label.configure(wraplength=self.steps.winfo_width() - 50)
                if self.ste_font_size >= 5 and self.ste_font_size <= 40:
                    font_size = 26 - 2 * self.n_steps
                    if font_size < 5:
                        font_size = 10
                    ste.configure(font=("Arial", font_size))
