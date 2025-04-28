import os
from unittest import TestCase
from io import StringIO
import json

from controllers.recipes import add_recipe, get_recipe, delete_recipe
from models import Recipe


class TestRecipeCommands(TestCase):
    def setUp(self) -> None:
        os.environ["RECIPE_DATA_PATH"] = "./tests/test_data_output.json"
        self.carnitas_recipe_data = {
            "category": "mexican",
            "title": "Carnitas",
            "slug": "carnitas",
            "image_urls": ["https://carnitas.com/jpg"],
        }
        self.salad_recipe_data = {
            "category": "salads",
            "title": "Big Salad",
            "slug": "big-salad",
            "image_urls": ["https://big-salad.com/png"],
        }

    def test_add_recipe(self):
        recipe = Recipe(**self.carnitas_recipe_data)
        recipe_data_file = StringIO()
        recipe_data_file.write(json.dumps([self.salad_recipe_data]))
        recipe_data_file.seek(0)
        result = add_recipe(recipe_data_file, recipe)
        recipe_data_file.seek(0)
        self.assertEqual(recipe, result)
        self.assertEqual(
            json.load(recipe_data_file),
            [self.salad_recipe_data, self.carnitas_recipe_data],
        )

    def test_get_recipe(self):
        recipe_data = [self.carnitas_recipe_data]
        expected = Recipe(**recipe_data[0])
        recipe = get_recipe("carnitas", recipe_data)
        self.assertEqual(recipe, expected)

    def test_delete_recipe(self):
        recipe_data = [self.carnitas_recipe_data, self.salad_recipe_data]
        expected_data = [self.salad_recipe_data]
        recipe_data_file = StringIO()
        recipe_data_file.write(json.dumps(recipe_data))
        recipe_data_file.seek(0)
        slug = "carnitas"

        initial_data = json.load(recipe_data_file)
        self.assertEqual(initial_data, recipe_data)
        self.assertTrue(delete_recipe(slug, recipe_data_file))
        recipe_data_file.seek(0)
        resulting_data = json.load(recipe_data_file)
        self.assertEqual(resulting_data, expected_data)
