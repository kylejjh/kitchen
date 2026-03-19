from backend.app.main import create_app


def test_create_cuisine(client):
    payload = {
        "name": "Chinese",
        "description": "Chinese cuisine"
    }

    response = client.post("/cuisines", json=payload)

    assert response.status_code == 201
    data = response.get_json()
    assert data["name"] == "Chinese"
    assert data["description"] == "Chinese cuisine"
    assert "_id" in data


def test_get_all_cuisines(client):
    client.post("/cuisines", json={
        "name": "Italian",
        "description": "Italian cuisine"
    })

    client.post("/cuisines", json={
        "name": "Japanese",
        "description": "Japanese cuisine"
    })

    response = client.get("/cuisines")

    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) >= 2


def test_get_one_cuisine(client):
    create_response = client.post("/cuisines", json={
        "name": "Mexican",
        "description": "Mexican cuisine"
    })
    created = create_response.get_json()
    cuisine_id = created["_id"]

    response = client.get(f"/cuisines/{cuisine_id}")

    assert response.status_code == 200
    data = response.get_json()
    assert data["_id"] == cuisine_id
    assert data["name"] == "Mexican"


def test_update_cuisine(client):
    create_response = client.post("/cuisines", json={
        "name": "Thai",
        "description": "Thai cuisine"
    })
    created = create_response.get_json()
    cuisine_id = created["_id"]

    response = client.put(f"/cuisines/{cuisine_id}", json={
        "name": "Thai Updated",
        "description": "Updated description"
    })

    assert response.status_code == 200
    data = response.get_json()
    assert data["name"] == "Thai Updated"
    assert data["description"] == "Updated description"


def test_delete_cuisine(client):
    create_response = client.post("/cuisines", json={
        "name": "Indian",
        "description": "Indian cuisine"
    })
    created = create_response.get_json()
    cuisine_id = created["_id"]

    delete_response = client.delete(f"/cuisines/{cuisine_id}")
    assert delete_response.status_code == 200

    get_response = client.get(f"/cuisines/{cuisine_id}")
    assert get_response.status_code == 404
