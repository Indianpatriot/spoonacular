import requests
from logging_config import logger

API_KEY = "fa456475706b443a99fc843f3077688e"
BASE_URL = "https://api.spoonacular.com/recipes"

# ✅ Add this function
def fetch_recipes(ingredient, diet="none"):
    try:
        url = f"{BASE_URL}/complexSearch"
        params = {
            "apiKey": API_KEY,
            "query": ingredient,
            "number": 10,
            "addRecipeInformation": True,
            "instructionsRequired": True
        }

        if diet != "none":
            params["diet"] = diet

        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        return data.get("results", [])

    except requests.RequestException as e:
        logger.error(f"Error fetching recipes: {e}")
        return []

# ✅ Already present
def fetch_recipe_details(recipe_id):
    try:
        url = f"{BASE_URL}/{recipe_id}/information"
        params = {
            "includeNutrition": "true",
            "apiKey": API_KEY
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        important_nutrients = ["Protein", "Calories", "Fat", "Carbohydrates"]
        all_nutrients = data.get("nutrition", {}).get("nutrients", [])

        filtered_nutrients = [
            n for n in all_nutrients if n.get("name") in important_nutrients
        ]

        data["nutrition"]["filtered_nutrients"] = filtered_nutrients
        return data

    except requests.RequestException as e:
        logger.error(f"Error fetching recipe details: {e}")
        return {}
