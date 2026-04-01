from __future__ import annotations

from bson import ObjectId
from flask import request
from flask_restx import Namespace, Resource, fields

from backend.app.db import get_db

ingredients_ns = Namespace("ingredients", description="Ingredients CRUD")

ingredient_model = ingredients_ns.model(
    "Ingredient",
    {
        "id": fields.String(readOnly=True, description="Mongo ObjectId as string"),
        "name": fields.String(required=True, description="Ingredient name"),
        "category": fields.String(required=False, description="Optional category"),
        "notes": fields.String(required=False, description="Optional notes"),
    },
)

ingredient_create_model = ingredients_ns.model(
    "IngredientCreate",
    {
        "name": fields.String(required=True),
        "category": fields.String(required=False),
        "notes": fields.String(required=False),
    },
)

ingredient_update_model = ingredients_ns.model(
    "IngredientUpdate",
    {
        "name": fields.String(required=False),
        "category": fields.String(required=False),
        "notes": fields.String(required=False),
    },
)


def _to_public(doc: dict) -> dict:
    """Convert Mongo document to API-safe dict."""
    return {
        "id": str(doc["_id"]),
        "name": doc.get("name", ""),
        "category": doc.get("category"),
        "notes": doc.get("notes"),
    }


def _parse_object_id(id_str: str) -> ObjectId:
    try:
        return ObjectId(id_str)
    except Exception as e:
        raise ValueError("Invalid id") from e


@ingredients_ns.route("")
class IngredientsCollection(Resource):
    @ingredients_ns.marshal_list_with(ingredient_model)
    def get(self):
        return [
            {"id": "1", "name": "Tomato", "category": "Vegetable"},
            {"id": "2", "name": "Egg", "category": "Protein"},
            {"id": "3", "name": "Chicken", "category": "Meat"},
        ], 200

    @ingredients_ns.expect(ingredient_create_model, validate=True)
    @ingredients_ns.marshal_with(ingredient_model, code=201)
    def post(self):
        payload = request.get_json(force=True) or {}
        name = (payload.get("name") or "").strip()
        if not name:
            ingredients_ns.abort(400, "name is required")

        doc = {
            "name": name,
            "category": (payload.get("category") or "").strip() or None,
            "notes": (payload.get("notes") or "").strip() or None,
        }

        db = get_db()
        result = db.ingredients.insert_one(doc)
        saved = db.ingredients.find_one({"_id": result.inserted_id})
        return _to_public(saved), 201


@ingredients_ns.route("/<string:ingredient_id>")
class IngredientItem(Resource):
    @ingredients_ns.marshal_with(ingredient_model)
    def get(self, ingredient_id: str):
        try:
            oid = _parse_object_id(ingredient_id)
        except ValueError:
            ingredients_ns.abort(400, "Invalid id")

        db = get_db()
        doc = db.ingredients.find_one({"_id": oid})
        if not doc:
            ingredients_ns.abort(404, "Ingredient not found")
        return _to_public(doc), 200

    @ingredients_ns.expect(ingredient_update_model, validate=True)
    @ingredients_ns.marshal_with(ingredient_model)
    def put(self, ingredient_id: str):
        try:
            oid = _parse_object_id(ingredient_id)
        except ValueError:
            ingredients_ns.abort(400, "Invalid id")

        payload = request.get_json(force=True) or {}
        update: dict = {}

        if "name" in payload:
            name = (payload.get("name") or "").strip()
            if not name:
                ingredients_ns.abort(400, "name cannot be empty")
            update["name"] = name

        if "category" in payload:
            update["category"] = (payload.get("category") or "").strip() or None

        if "notes" in payload:
            update["notes"] = (payload.get("notes") or "").strip() or None

        if not update:
            ingredients_ns.abort(400, "No fields provided to update")

        db = get_db()
        res = db.ingredients.update_one({"_id": oid}, {"$set": update})
        if res.matched_count == 0:
            ingredients_ns.abort(404, "Ingredient not found")

        doc = db.ingredients.find_one({"_id": oid})
        return _to_public(doc), 200

    def delete(self, ingredient_id: str):
        try:
            oid = _parse_object_id(ingredient_id)
        except ValueError:
            ingredients_ns.abort(400, "Invalid id")

        db = get_db()
        res = db.ingredients.delete_one({"_id": oid})
        if res.deleted_count == 0:
            ingredients_ns.abort(404, "Ingredient not found")
        return {"deleted": True, "id": ingredient_id}, 200
