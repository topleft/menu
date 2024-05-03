# Menu

A website to organize a library of recipes captured as images and pdfs.

## Add Recipes

Add recipe images to s3 and write new gatsby data.

```sh
cd menu-cli

poetry run menu recipe add -p ./path/to/recipe.json
```

## Deploy

```sh
npm run build

npm run deploy
```