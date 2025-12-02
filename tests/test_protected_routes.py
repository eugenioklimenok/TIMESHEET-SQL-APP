
def test_accounts_requires_token(client):
    response = client.get("/accounts/")
    assert response.status_code == 401


def test_timesheets_requires_token(client):
    response = client.get("/timesheets/")
    assert response.status_code == 401
