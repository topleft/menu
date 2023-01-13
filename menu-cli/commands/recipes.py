import os
import json
from pathlib import Path

import typer
from pydantic import ValidationError
from slugify import slugify

from models import RecipeInput, Recipe
from controllers.recipes import (
    get_recipe_data_path,
    upload_recipe_images,
    get_recipe,
    delete_recipe,
    add_recipe,
)

app = typer.Typer()


@app.command()
def add(
    recipe_input_path: Path = typer.Option(
        ..., "-p", help="path to json of Recipes for adding"
    )
):
    # TODO consolidate file IO
    with open(recipe_input_path, "r") as json_data:
        recipes_input = json.load(json_data)

        recipe_data_path = get_recipe_data_path()
        print(recipe_data_path)

        for r in recipes_input:
            try:
                recipe_input = RecipeInput(**r)
            except ValidationError as e:
                print(e.json())
                continue

            if not recipe_input.slug:
                recipe_input.slug = slugify(recipe_input.title)

            print(f"\nAdding recipe for {recipe_input.slug}")

            with open(recipe_data_path, "r") as f:
                recipe_data = json.load(f)
                existing_recipe = get_recipe(recipe_input.slug, recipe_data)

            if existing_recipe:
                print(f'Existing recipe found for slug "{recipe_input.slug}"')
                update = typer.confirm("Update?")
                if not update:
                    print(f"Skipped {recipe_input.slug}.")
                    continue
                else:
                    # remove recipe from json so it is not duplicated
                    with open(recipe_data_path, "r+") as f:
                        delete_recipe(existing_recipe.slug, f)

            print(f"Uploading image(s)")

            image_urls = upload_recipe_images(
                recipe_input.slug, recipe_input.image_paths
            )

            if not len(image_urls) == len(recipe_input.image_paths):
                print(f"Warning. Failed to upload all images for {recipe_input.slug}.")
                print(
                    f"{len(image_urls)}/{len(recipe_input.image_paths)} successfully uploaded."
                )

            recipe = Recipe(
                category=recipe_input.category,
                title=recipe_input.title,
                slug=recipe_input.slug,
                image_urls=image_urls,
            )

            print("Writing json data to file")
            with open(recipe_data_path, "r+") as f:
                add_recipe(f, recipe)

            print(f"Recipe '{recipe.slug}' added!")

    print(f"\nDone.")


@app.command()
def get(slug: str = typer.Option(None, "-s", help="Slug of recipe")):
    recipe_data_path = get_recipe_data_path()
    with open(recipe_data_path, "r") as f:
        recipe_data = json.load(f)
        recipe = get_recipe(slug, recipe_data)

    if recipe:
        print(f"Recipe found: {slug}")
        print(recipe)
    else:
        print(f"No recipe found with slug: {slug}")


@app.command()
def delete(slug: str = typer.Option(None, "-s", help="Slug of recipe")):
    recipe_data_path = get_recipe_data_path()
    with open(recipe_data_path, "r+") as f:
        success = delete_recipe(slug, f)
    if success:
        print(f"Deleted recipe: {slug}")
    else:
        print(f"Did not delete recipe. No recipe found with slug: {slug}")


if __name__ == "__main__":
    app()
