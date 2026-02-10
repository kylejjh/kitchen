from flask import Flask, request
from flask_restx import Api, Namespace, Resource
from bson import ObjectId
from backend.app.db import ping_mongo, get_db


def create_app() -> Flask:
    app = Flask(__name__)
    api = Api(app, title="Kitchen API", version="0.1")


    health_ns = Namespace("health", description="Health check")

    @health_ns.route("")
    class Health(Resource):
        def get(self):
            return {"status": "ok"}, 200

        

    db_ns = Namespace("db", description="Database check")
    
    @db_ns.route("/health")
    class DbHealth(Resource):
        def get(self):
            ok = ping_mongo()
            return {"mongo": "ok" if ok else "down"}, 200 if ok else 500



    recipes_ns = Namespace("recipes", description="Recipe management")

    def _serialize_recipe(doc: dict) -> dict:
        # Convert Mongo ObjectId to string so it can be JSON serialized
        doc["_id"] = str(doc["_id"])
        return doc



    @recipes_ns.route("")
    class Recipes(Resource):
        def get(self):
            db = get_db()
            docs = list(db.recipes.find().sort("_id", -1))
            return {"recipes": [_serialize_recipe(d) for d in docs]}, 200

        def post(self):
            data = request.get_json(silent=True) or {}

            name = data.get("name")
            if not isinstance(name, str) or not name.strip():
                return {"error": "Field 'name' is required and must be a non-empty string."}, 400

            recipe = {
                "name": name.strip(),
                "ingredients": data.get("ingredients", []),
                "steps": data.get("steps", []),
                "tags": data.get("tags", []),
            }

            db = get_db()
            result = db.recipes.insert_one(recipe)
            created = db.recipes.find_one({"_id": result.inserted_id})
            return _serialize_recipe(created), 201



    @recipes_ns.route("/<string:recipe_id>")
    class RecipeById(Resource):
        def get(self, recipe_id: str):
            # Validate ObjectId format
            try:
                oid = ObjectId(recipe_id)
            except Exception:
                return {"error": "Invalid recipe id format."}, 400

            db = get_db()
            doc = db.recipes.find_one({"_id": oid})
            if doc is None:
                return {"error": "Recipe not found."}, 404

            return _serialize_recipe(doc), 200


        def patch(self, recipe_id: str):
            # Validate ObjectId format
            try:
                oid = ObjectId(recipe_id)
            except Exception:
                return {"error": "Invalid recipe id format."}, 400

            data = request.get_json(silent=True) or {}
            if not isinstance(data, dict):
                return {"error": "Request body must be a JSON object."}, 400

            allowed_fields = {"name", "ingredients", "steps", "tags"}
            update = {}

            for key in data:
                if key not in allowed_fields:
                    return {"error": f"Field '{key}' is not updatable."}, 400

            # Validate + build update dict
            if "name" in data:
                name = data["name"]
                if not isinstance(name, str) or not name.strip():
                    return {"error": "Field 'name' must be a non-empty string."}, 400
                update["name"] = name.strip()

            for field in ("ingredients", "steps", "tags"):
                if field in data:
                    val = data[field]
                    if not isinstance(val, list) or not all(isinstance(x, str) for x in val):
                        return {"error": f"Field '{field}' must be a list of strings."}, 400
                    update[field] = val

            if not update:
                return {"error": "No valid fields provided to update."}, 400

            db = get_db()
            result = db.recipes.update_one({"_id": oid}, {"$set": update})
            if result.matched_count == 0:
                return {"error": "Recipe not found."}, 404

            doc = db.recipes.find_one({"_id": oid})
            return _serialize_recipe(doc), 200


        def delete(self, recipe_id: str):
            # Validate ObjectId format
            try:
                oid = ObjectId(recipe_id)
            except Exception:
                return {"error": "Invalid recipe id format."}, 400

            db = get_db()
            result = db.recipes.delete_one({"_id": oid})
            if result.deleted_count == 0:
                return {"error": "Recipe not found."}, 404

            return {"deleted": True, "id": recipe_id}, 200

        

    api.add_namespace(db_ns, path="/db")
    api.add_namespace(health_ns, path="/health")
    api.add_namespace(recipes_ns, path="/recipes")


    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
