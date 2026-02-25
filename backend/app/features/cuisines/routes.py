# backend/app/features/cuisines/routes.py
from flask import request
from flask_restx import Namespace, Resource

from bson import ObjectId
from backend.app.db import get_db

cuisines_ns = Namespace("cuisines", description="Cuisine management")


def _serialize_cuisine(doc: dict) -> dict:
    doc["_id"] = str(doc["_id"])
    return doc


def _slugify(name: str) -> str:
    # simple slug: "Chinese Food" -> "chinese-food"
    s = (name or "").strip().lower()
    s = "-".join(s.split())
    # keep only letters, numbers, dashes
    s = "".join(ch for ch in s if ch.isalnum() or ch == "-")
    return s


@cuisines_ns.route("")
class Cuisines(Resource):
    def get(self):
        db = get_db()

        # Optional: filter by slug
        slug = request.args.get("slug")
        query = {}
        if slug:
            query["slug"] = slug.strip().lower()

        docs = list(db.cuisines.find(query).sort("_id", -1))
        return {"cuisines": [_serialize_cuisine(d) for d in docs]}, 200

    def post(self):
        data = request.get_json(silent=True) or {}
        if not isinstance(data, dict):
            return {"error": "Request body must be a JSON object."}, 400

        name = data.get("name")
        if not isinstance(name, str) or not name.strip():
            return {"error": "Field 'name' is required and must be a non-empty string."}, 400
        name = name.strip()

        slug = data.get("slug")
        if slug is None:
            slug = _slugify(name)
        if not isinstance(slug, str) or not slug.strip():
            return {"error": "Field 'slug' must be a non-empty string if provided."}, 400
        slug = slug.strip().lower()

        region = data.get("region", "")
        if region is not None and not isinstance(region, str):
            return {"error": "Field 'region' must be a string."}, 400

        db = get_db()

        # Basic uniqueness check on slug
        if db.cuisines.find_one({"slug": slug}) is not None:
            return {"error": f"Cuisine slug '{slug}' already exists."}, 409

        cuisine = {
            "name": name,
            "slug": slug,
            "region": region or "",
        }

        result = db.cuisines.insert_one(cuisine)
        created = db.cuisines.find_one({"_id": result.inserted_id})
        return _serialize_cuisine(created), 201


@cuisines_ns.route("/<string:cuisine_id>")
class CuisineById(Resource):
    def get(self, cuisine_id: str):
        try:
            oid = ObjectId(cuisine_id)
        except Exception:
            return {"error": "Invalid cuisine id format."}, 400

        db = get_db()
        doc = db.cuisines.find_one({"_id": oid})
        if doc is None:
            return {"error": "Cuisine not found."}, 404
        return _serialize_cuisine(doc), 200

    def patch(self, cuisine_id: str):
        try:
            oid = ObjectId(cuisine_id)
        except Exception:
            return {"error": "Invalid cuisine id format."}, 400

        data = request.get_json(silent=True) or {}
        if not isinstance(data, dict):
            return {"error": "Request body must be a JSON object."}, 400

        allowed_fields = {"name", "slug", "region"}
        for key in data:
            if key not in allowed_fields:
                return {"error": f"Field '{key}' is not updatable."}, 400

        update = {}

        if "name" in data:
            name = data["name"]
            if not isinstance(name, str) or not name.strip():
                return {"error": "Field 'name' must be a non-empty string."}, 400
            update["name"] = name.strip()

        if "slug" in data:
            slug = data["slug"]
            if not isinstance(slug, str) or not slug.strip():
                return {"error": "Field 'slug' must be a non-empty string."}, 400
            slug = slug.strip().lower()

            db = get_db()
            existing = db.cuisines.find_one({"slug": slug, "_id": {"$ne": oid}})
            if existing is not None:
                return {"error": f"Cuisine slug '{slug}' already exists."}, 409

            update["slug"] = slug

        if "region" in data:
            region = data["region"]
            if region is not None and not isinstance(region, str):
                return {"error": "Field 'region' must be a string."}, 400
            update["region"] = region or ""

        if not update:
            return {"error": "No valid fields provided to update."}, 400

        db = get_db()
        result = db.cuisines.update_one({"_id": oid}, {"$set": update})
        if result.matched_count == 0:
            return {"error": "Cuisine not found."}, 404

        doc = db.cuisines.find_one({"_id": oid})
        return _serialize_cuisine(doc), 200

    def delete(self, cuisine_id: str):
        try:
            oid = ObjectId(cuisine_id)
        except Exception:
            return {"error": "Invalid cuisine id format."}, 400

        db = get_db()
        result = db.cuisines.delete_one({"_id": oid})
        if result.deleted_count == 0:
            return {"error": "Cuisine not found."}, 404

        return {"deleted": True, "id": cuisine_id}, 200
