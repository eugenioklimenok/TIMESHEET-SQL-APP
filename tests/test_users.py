from uuid import UUID


def test_create_and_list_users(client):
    payload = {
        "user_id": "u001",
        "name": "Test User",
        "email": "user@example.com",
        "profile": "tester",
        "role": "admin",
    }

    create_response = client.post("/users/", json=payload)
    assert create_response.status_code == 201
    body = create_response.json()
    assert UUID(body["id"])
    assert body["email"] == payload["email"]

    list_response = client.get("/users/")
    assert list_response.status_code == 200
    users = list_response.json()
    assert len(users) == 1
    assert users[0]["user_id"] == payload["user_id"]
