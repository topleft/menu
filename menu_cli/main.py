import typer
from commands.recipes import app as recipe_commands


app = typer.Typer(name="menu", help="What's on the menu!?")

app.add_typer(recipe_commands, name="recipe")
