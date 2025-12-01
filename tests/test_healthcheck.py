from app.main import app


def test_healthcheck(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.json()["message"] == "TimeSheet App API funcionando"
