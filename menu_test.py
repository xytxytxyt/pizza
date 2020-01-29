import unittest
import uuid

import menu as menu_module


class MenuTest(unittest.TestCase):
    def test_generate_menu_item_id_without_seed(self):
        menu = menu_module.Menu(
            n_pizzas=5,
            n_sides=5,
            n_drinks=5
        )
        menu_item_id = menu.generate_menu_item_id()
        uuid.UUID(str(menu_item_id))  # assert valid uuid generated

    def test_generate_menu_item_id_with_seed(self):
        menu = menu_module.Menu(
            n_pizzas=5,
            n_sides=5,
            n_drinks=5,
            random_seed=0
        )

        menu_item_id = menu.generate_menu_item_id()
        self.assertEqual(str(menu_item_id), '85776e9a-dd84-f39e-7154-5a137a1d5006')
        menu_item_id = menu.generate_menu_item_id()
        self.assertEqual(str(menu_item_id), 'eb2083e6-ce16-4dba-0ff1-8e0242af9fc3')
        menu_item_id = menu.generate_menu_item_id()
        self.assertEqual(str(menu_item_id), '17e0aa3c-0398-3ca8-ea7e-9d498c778ea6')
        menu_item_id = menu.generate_menu_item_id()
        self.assertEqual(str(menu_item_id), 'b5d32b16-6619-4cb1-d710-37d1b83e90ec')
        menu_item_id = menu.generate_menu_item_id()
        self.assertEqual(str(menu_item_id), 'a0116be5-ab0c-1681-c8f8-e3d0d3290a4c')

    def test_generate_menu(self):
        menu = menu_module.Menu(
            n_pizzas=5,
            n_sides=5,
            n_drinks=5,
            random_seed=0
        )

        self.assertEqual(str(menu.menu['pizzas'][0][0]), 'e3e70682-c209-4cac-629f-6fbed82c07cd')
        self.assertEqual(str(menu.menu['pizzas'][1][0]), 'f728b4fa-4248-5e3a-0a5d-2f346baa9455')
        self.assertEqual(str(menu.menu['pizzas'][2][0]), 'eb1167b3-67a9-c378-7c65-c1e582e2e662')
        self.assertEqual(str(menu.menu['pizzas'][3][0]), 'f7c1bd87-4da5-e709-d471-3d60c8a70639')
        self.assertEqual(str(menu.menu['pizzas'][4][0]), 'e443df78-9558-867f-5ba9-1faf7a024204')


if __name__ == '__main__':
    unittest.main()
