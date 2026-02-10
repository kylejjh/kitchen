import argparse
from backend.app.db import get_db

SAMPLE_RECIPES = [
    {
        "name": "Tomato Egg",
        "ingredients": ["tomato", "egg", "salt", "oil"],
        "steps": ["cut tomato", "fry egg", "stir-fry tomato", "mix and season"],
        "tags": ["Chinese", "quick", "home-cooking"],
    },
    {
        "name": "Garlic Butter Pasta",
        "ingredients": ["pasta", "garlic", "butter", "salt", "black pepper"],
        "steps": ["boil pasta", "melt butter", "saute garlic", "toss pasta", "season"],
        "tags": ["quick"],
    },
    {
        "name": "Oatmeal Bowl",
        "ingredients": ["oats", "milk", "banana", "honey"],
        "steps": ["cook oats with milk", "slice banana", "top with honey"],
        "tags": ["breakfast", "healthy"],
    },
]

def main():
    parser = argparse.ArgumentParser(description="Load sample recipes into MongoDB.")
    parser.add_argument("--wipe", action="store_true", help="Delete all existing recipes before loading.")
    args = parser.parse_args()

    db = get_db()

    if args.wipe:
        deleted = db.recipes.delete_many({}).deleted_count
        print(f"Wiped recipes collection: deleted {deleted} docs")

    result = db.recipes.insert_many(SAMPLE_RECIPES)
    print(f"Inserted {len(result.inserted_ids)} recipes into db '{db.name}', collection 'recipes'")

if __name__ == "__main__":
    main()
