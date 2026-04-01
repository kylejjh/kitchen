def test_create_cuisine(client):
    payload = {
        "name": "Chinese"
    }

    response = client.post("/cuisines", json=payload)

    assert response.status_code == 201
    data = response.get_json()

    assert data["name"] == "Chinese"
    assert "slug" in data
    assert "_id" in data


def test_get_all_cuisines(client):
    client.post("/cuisines", json={"name": "Italian"})
    client.post("/cuisines", json={"name": "Japanese"})

    response = client.get("/cuisines")

    assert response.status_code == 200
    data = response.get_json()

    assert "cuisines" in data
    assert isinstance(data["cuisines"], list)
    assert len(data["cuisines"]) >= 2


def test_update_cuisine(client):
    create_response = client.post("/cuisines", json={"name": "Thai"})
    created = create_response.get_json()
    cuisine_id = created["_id"]

    response = client.patch(
        f"/cuisines/{cuisine_id}",
        json={"name": "Thai Updated"}
    )

    assert response.status_code == 200
    data = response.get_json()

    assert data["name"] == "Thai Updated"
