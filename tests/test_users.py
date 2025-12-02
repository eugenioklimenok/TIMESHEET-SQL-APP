def test_create_and_list_users(client, user_payload):
    create_response = client.post("/users/", json=user_payload)
    assert create_response.status_code == 201

    login_response = client.post(
        "/auth/login", data={"username": user_payload["email"], "password": user_payload["password"]}
    )
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    list_response = client.get("/users/", headers={"Authorization": f"Bearer {token}"})
    assert list_response.status_code == 200
    users = list_response.json()
    assert len(users) == 1
    assert users[0]["user_id"] == user_payload["user_id"]


def test_protected_users_requires_token(client):
    response = client.get("/users/")
    assert response.status_code == 401
