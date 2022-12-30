import os
import json
from typing import TextIO

from pathlib import Path


from utils import get_content_type, upload_image
from models import Recipe

CLOUDFRONT_URL = os.environ.get(
    "CLOUDFRONT_URL", "https://db1kxxvrlszby.cloudfront.net"
)
BUCKET = os.environ.get("IMAGES_BUCKET", "topleft-menu-images")


def get_recipe_data_path():
    RECIPE_DATA_PATH = os.environ.get("RECIPE_DATA_PATH", "../../src/data/recipes.json")
    dirname = os.path.dirname(__file__)
    return os.path.join(dirname, RECIPE_DATA_PATH)


def get_recipe(slug: str, recipe_data: list) -> Recipe:
    for recipe in recipe_data:
        if recipe["slug"] == slug:
            return Recipe(**recipe)
    return None


def add_recipe(recipe_data_file: TextIO, recipe: Recipe) -> None:
    recipe_data = json.load(recipe_data_file)
    recipe_data_file.seek(0)
    recipe_data.append(recipe.dict())
    json.dump(recipe_data, recipe_data_file, ensure_ascii=False, indent=2)
    return recipe


def delete_recipe(slug: str, recipe_data_file: TextIO) -> None:
    recipe_data_file.seek(0)
    recipe_data = json.load(recipe_data_file)
    recipe_data_file.seek(0)
    recipe_data_file.truncate(0)
    for i, recipe in enumerate(recipe_data):
        if recipe["slug"] == slug:
            del recipe_data[i]
            json.dump(recipe_data, recipe_data_file, ensure_ascii=False, indent=2)
            return True
    return False


def upload_recipe_images(slug: str, image_paths: list[Path]) -> list[str]:
    image_urls = []
    for i, image_path in enumerate(image_paths):
        object_key = f"{slug}_{i+1}{image_path.suffix}"
        content_type = get_content_type(Path(image_path))
        if content_type is None:
            print(
                f"Warning: Could not determine content type for file {image_path}. Not uploading image. "
            )
            continue

        upload_success = upload_image(
            BUCKET, object_key, image_path, slug, content_type
        )
        print(f"File uploaded: {upload_success}")
        url = f"{CLOUDFRONT_URL}/{object_key}"
        print(url)

        if upload_success:
            image_urls.append(url)
    return image_urls
