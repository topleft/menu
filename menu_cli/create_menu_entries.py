from pathlib import Path
from datetime import datetime
from models import RecipeInput
import json


def compile_images_into_recipes(folder_path: Path) -> dict:
    compiled_recipes = {}
    folder = folder_path.iterdir()
    for folder_item in folder:
        if not folder_item.is_dir():
            print(f"Expected a folder, got {folder_item}")
            continue
        if folder_item.name.lower() == ".ds_store":
            continue
        category = get_category(folder_item.name)
        if is_lewk(folder_item.name):
            compiled_recipes[get_slug(folder_item.stem)] = RecipeInput(
                category=category,
                title=get_title(folder_item.stem),
                slug=get_slug(folder_item.stem),
                image_paths=[clean_path(item) for item in folder_item.iterdir() if item.name.lower() != ".ds_store"],
            )
        else:
            for item in folder_item.iterdir():    
                if item.name.lower() == ".ds_store":
                    continue
                if compiled_recipes.get(get_slug(item.stem)):
                    compiled_recipes[get_slug(item.stem)].image_paths.append(clean_path(item))
                else:
                    compiled_recipes[get_slug(item.stem)] = RecipeInput(
                        category=category,
                        title=get_title(item.stem),
                        slug=get_slug(item.stem),
                        image_paths=[clean_path(item)],
                    )
    compiled_recipes = {k: json.loads(v.json()) for k, v in compiled_recipes.items()}
    return compiled_recipes


def get_category(folder_name: str) -> str:
    if "to_add" in folder_name:
        category = folder_name.replace("_to_add", "")
    elif "lewk" in folder_name:
        category = folder_name.replace("_lewk", "")
        if "italian" in category:
            category = "italian"
            
    else:
        raise ValueError(f"Could not find category in {folder_name}")
    return category

def get_slug(name):
    try:
        if int(name[-1]):
            name = name[:-2]
    except ValueError:
        pass
    return name.lower().replace(" ", "-").replace("_", "-") 


def get_title(name):
    try:    
        if int(name[-1]):
            name = name[:-2]
    except ValueError:
        pass
    return name.replace("-", " ").replace("_", " ").title()

def clean_path(path: Path) -> Path:
    if " " in path.name:
        new_name = path.name.replace(" ", "_")
        path.rename(path.parent / new_name)
    return path.absolute()


def is_lewk(name):
    return "lewk" in name

if __name__ == "__main__":
    # read file        
    folder_path = Path("./menu_cli/menu_2024_09_15")
    compiled_recipes = compile_images_into_recipes(folder_path)
    input_data = [item for item in compiled_recipes.values()]
    print(input_data)
    #  write to file
    date = datetime.now().strftime("%Y%m%d")
    with open(f"./menu_cli/input_data/{date}.json", "w") as f:
        f.write(json.dumps(input_data))
