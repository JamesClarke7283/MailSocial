# ./src/utils.py
# src/utils.py
import tomllib

with open(".default_settings.toml", "rb") as f:
    config = tomllib.load(f)

themes = config["appearance"]["themes"]
theme_names = [theme.capitalize() for theme in themes.keys()]

def get_theme_colors(theme_name):
    return themes[theme_name.lower()]

def get_accents():
    accents = config["appearance"]["accents"]
    return {name: data["color"] for name, data in accents.items()}

def get_default_button_color(theme_name):
    return themes[theme_name.lower()]["button"]
