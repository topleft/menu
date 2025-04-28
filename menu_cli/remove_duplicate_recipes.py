import json
import os


with open("/Users/pete.jeffryes/Documents/pete/menu/src/data/recipes.json", "r") as f:
    recipes = json.load(f)
    print(len(recipes))
    recipes_to_remove =  []
    for r in recipes:
        if any([ s in r["slug"] for s in [".jpeg", ".jpg", ".png"]]) > 0:
            print("removing recipe")
            recipes_to_remove.append(r)
    dedupe_recipes = list(set([json.dumps(r) for r in recipes]) - set(json.dumps(r) for r in recipes_to_remove))
    print(len(dedupe_recipes))

with open("/Users/pete.jeffryes/Documents/pete/menu/src/data/dedupe_recipes.json", "w") as f:
    f.write(json.dumps([json.loads(r) for r in dedupe_recipes], indent=4))
