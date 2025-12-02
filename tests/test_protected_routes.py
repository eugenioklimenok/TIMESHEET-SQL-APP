
def test_accounts_requires_token(client):
    response = client.get("/accounts/")
    assert response.status_code == 401


def test_timesheets_requires_token(client):
    response = client.get("/timesheets/")
    assert response.status_code == 401


def test_accounts_requires_admin_role(client, user_headers):
    response = client.get("/accounts/", headers=user_headers)
    assert response.status_code == 403


def test_accounts_allows_admin(client, auth_headers):
    response = client.get("/accounts/", headers=auth_headers)
    assert response.status_code == 200


def test_timesheets_allow_user_role(client, user_headers):
    response = client.get("/timesheets/", headers=user_headers)
    assert response.status_code == 200
