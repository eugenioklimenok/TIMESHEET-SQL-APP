def test_create_and_list_users(client, auth_headers, user_payload):
    create_response = client.post("/users/", json=user_payload, headers=auth_headers)
    assert create_response.status_code == 201

    list_response = client.get("/users/", headers=auth_headers)
    assert list_response.status_code == 200
    users = list_response.json()
    assert len(users) == 1
    assert users[0]["user_id"] == user_payload["user_id"]


def test_protected_users_requires_token(client):
    response = client.get("/users/")
    assert response.status_code == 401


def test_user_role_cannot_access_admin_routes(client, user_headers):
    response = client.get("/users/", headers=user_headers)
    assert response.status_code == 403
