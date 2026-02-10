from backend.app.main import create_app
from backend.app.db import get_db

def _client():
    app = create_app()
    return app.test_client()

def _clear_recipes():
    db = get_db()
    db.recipes.delete_many({})

def test_post_recipe_creates_and_returns_recipe():
    _clear_recipes()
    client = _client()

    payload = {
        "name": "Tomato Egg",
        "ingredients": ["tomato", "egg", "salt"],
        "steps": ["cut tomato", "fry egg", "mix"],
        "tags": ["quick", "Chinese"],
    }

    resp = client.post("/recipes", json=payload)
    assert resp.status_code == 201

    data = resp.get_json()
    assert "_id" in data
    assert data["name"] == "Tomato Egg"
    assert data["ingredients"] == ["tomato", "egg", "salt"]
    assert data["steps"] == ["cut tomato", "fry egg", "mix"]
    assert data["tags"] == ["quick", "Chinese"]

def test_get_recipes_returns_list():
    _clear_recipes()
    client = _client()

    # create two recipes
    r1 = client.post("/recipes", json={"name": "A"}).get_json()
    r2 = client.post("/recipes", json={"name": "B"}).get_json()

    resp = client.get("/recipes")
    assert resp.status_code == 200

    data = resp.get_json()
    assert "recipes" in data
    assert isinstance(data["recipes"], list)

    ids = [r["_id"] for r in data["recipes"]]
    assert r1["_id"] in ids
    assert r2["_id"] in ids

def test_get_recipe_by_id_success_and_404():
    _clear_recipes()
    client = _client()

    created = client.post("/recipes", json={"name": "Tomato Egg"}).get_json()
    rid = created["_id"]

    resp = client.get(f"/recipes/{rid}")
    assert resp.status_code == 200
    assert resp.get_json()["_id"] == rid

    resp_missing = client.get("/recipes/000000000000000000000000")
    assert resp_missing.status_code == 404
    assert resp_missing.get_json()["error"] == "Recipe not found."

def test_patch_recipe_updates_fields():
    _clear_recipes()
    client = _client()

    created = client.post("/recipes", json={"name": "Old Name", "tags": ["x"]}).get_json()
    rid = created["_id"]

    resp = client.patch(f"/recipes/{rid}", json={"name": "New Name", "tags": ["y", "z"]})
    assert resp.status_code == 200

    updated = resp.get_json()
    assert updated["_id"] == rid
    assert updated["name"] == "New Name"
    assert updated["tags"] == ["y", "z"]

def test_delete_recipe_removes_it():
    _clear_recipes()
    client = _client()

    created = client.post("/recipes", json={"name": "To Delete"}).get_json()
    rid = created["_id"]

    resp = client.delete(f"/recipes/{rid}")
    assert resp.status_code == 200
    assert resp.get_json()["deleted"] is True

    # confirm gone
    resp2 = client.get(f"/recipes/{rid}")
    assert resp2.status_code == 404
