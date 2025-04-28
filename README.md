# Menu

A website to organize a library of recipes captured as images and pdfs.

## Add Recipes

Add recipe images to s3 and write new gatsby data.

```sh
cd menu-cli

poetry run menu recipe add -p ./path/to/recipes.json
```

*recipe.json is a list of RecipeInput json objects.

### RecipeInput
| key      | type           | description                                                                      |
| -------- | -------------- | -------------------------------------------------------------------------------- |
| category | Category       | Category to put recipe into. This will show up as a nav item in the Menu UI.     |
| title    | str            | Displayed as the list item in the category page and the title on the recipe page |
| slug     | kebab case str | used to name the image and in the url path                                       |


### Category

- 



## Deploy

```sh
npm run build

npm run deploy
```



