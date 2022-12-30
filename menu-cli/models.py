from typing import Optional
from pathlib import Path
from pydantic import BaseModel, AnyHttpUrl, validator


categories = ["salads", "italian", "mexican", "other", "israeli"]


class RecipeInput(BaseModel):
    category: str
    title: str
    slug: Optional[str] = None
    image_paths: list[Path]

    @validator("category")
    def category_is_lowercase(cls, v):
        category = v.lower()
        if category not in categories:
            print(f"Warning: Adding new category {category}")
        return category


class Recipe(BaseModel):
    category: str
    title: str
    slug: str
    image_urls: list[AnyHttpUrl]

    @validator("category")
    def category_is_lowercase(cls, v):
        category = v.lower()
        if category not in categories:
            print(f"Warning: Adding new category {category}")
        return category
