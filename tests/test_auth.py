
def test_login_returns_token(client, create_user, user_payload):
    create_user(user_payload)
    response = client.post(
        "/auth/login", data={"username": user_payload["email"], "password": user_payload["password"]}
    )
    assert response.status_code == 200
    body = response.json()
    assert body["access_token"]
    assert body["token_type"] == "bearer"


def test_auth_me_returns_current_user(client, auth_headers, admin_payload):
    response = client.get("/auth/me", headers=auth_headers)
    assert response.status_code == 200
    body = response.json()
    assert body["email"] == admin_payload["email"]
    assert body["user_id"] == admin_payload["user_id"]
