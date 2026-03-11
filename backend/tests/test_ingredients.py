def test_ingredients_crud(client):
    # Create
    res = client.post(
        "/ingredients",
        json={"name": "Garlic", "category": "vegetable", "notes": "fresh"},
    )
    assert res.status_code == 201
    created = res.get_json()
    assert created["name"] == "Garlic"
    assert "id" in created
    ingredient_id = created["id"]

    # List
    res = client.get("/ingredients")
    assert res.status_code == 200
    items = res.get_json()
    assert any(x["id"] == ingredient_id for x in items)

    # Get one
    res = client.get(f"/ingredients/{ingredient_id}")
    assert res.status_code == 200
    one = res.get_json()
    assert one["name"] == "Garlic"

    # Update
    res = client.put(f"/ingredients/{ingredient_id}", json={"notes": "minced"})
    assert res.status_code == 200
    updated = res.get_json()
    assert updated["notes"] == "minced"

    # Delete
    res = client.delete(f"/ingredients/{ingredient_id}")
    assert res.status_code == 200

    # Get again -> 404
    res = client.get(f"/ingredients/{ingredient_id}")
    assert res.status_code == 404
