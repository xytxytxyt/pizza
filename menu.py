import random
import uuid

import corporate


class Menu(object):
    def generate_menu(self):
        n_items = self.n_pizzas + self.n_sides + self.n_drinks
        adjectives = random.sample(corporate.corporate['adjectives'], self.n_pizzas)
        nouns = random.sample(corporate.corporate['nouns'], n_items)

        pizzas = []
        sides = []
        drinks = []

        i = 0
        for j in range(self.n_pizzas):
            menu_item_id = self.generate_menu_item_id()
            pizzas.append((str(menu_item_id), ' '.join([adjectives[i], nouns[i], 'pizza'])))
            self.menu_items.add(menu_item_id)
            i += 1
        for j in range(self.n_sides):
            menu_item_id = self.generate_menu_item_id()
            sides.append((str(menu_item_id), nouns[i]))
            self.menu_items.add(menu_item_id)
            i += 1
        for j in range(self.n_drinks):
            menu_item_id = self.generate_menu_item_id()
            drinks.append((str(menu_item_id), ' '.join([nouns[i], 'juice'])))
            self.menu_items.add(menu_item_id)
            i += 1

        return {
            "pizzas": pizzas,
            "sides": sides,
            "drinks": drinks,
        }

    def __init__(self, n_pizzas, n_sides, n_drinks, random_seed=None):
        self.n_pizzas = n_pizzas
        self.n_sides = n_sides
        self.n_drinks = n_drinks

        if random_seed is None:
            self.random_generator = None
        else:
            self.random_generator = random.Random()
            self.random_generator.seed(random_seed)

        self.menu_items = set()
        self.menu = self.generate_menu()

    def generate_menu_item_id(self):
        if self.random_generator is None:
            return uuid.uuid4()
        else:
            return uuid.UUID(int=self.random_generator.getrandbits(128))

    def is_valid_menu_item(self, menu_item_id):
        if isinstance(menu_item_id, str):
            menu_item_id = uuid.UUID(menu_item_id)
        return menu_item_id in self.menu_items
