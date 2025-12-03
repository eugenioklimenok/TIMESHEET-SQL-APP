import pytest


@pytest.fixture
def project_payload():
    return {
        "name": "Project Alpha",
        "code": "ALPHA001",
        "description": "Important project",
        "client_name": "Client A",
        "is_active": True,
    }


def test_admin_create_and_list_projects(client, auth_headers, project_payload):
    create_resp = client.post("/projects/", json=project_payload, headers=auth_headers)
    assert create_resp.status_code == 201
    project = create_resp.json()
    assert project["code"] == project_payload["code"]
    assert project["name"] == project_payload["name"]

    list_resp = client.get("/projects/", headers=auth_headers)
    assert list_resp.status_code == 200
    body = list_resp.json()
    assert body["total"] == 1
    assert body["limit"] == 25
    assert body["offset"] == 0
    assert body["results"][0]["id"] == project["id"]


def test_non_admin_cannot_create_project(client, user_headers, project_payload):
    response = client.post("/projects/", json=project_payload, headers=user_headers)
    assert response.status_code == 403
    assert response.json()["detail"] == "Only admins can perform this action"


def test_member_visibility_and_access(client, auth_headers, create_user, user_payload, project_payload):
    user = create_user(user_payload)
    login_resp = client.post(
        "/auth/login",
        data={"username": user_payload["email"], "password": user_payload["password"]},
    )
    user_token = login_resp.json()["access_token"]
    user_headers = {"Authorization": f"Bearer {user_token}"}

    project_one = client.post("/projects/", json=project_payload, headers=auth_headers).json()
    project_two = client.post(
        "/projects/",
        json={**project_payload, "code": "BETA001", "name": "Project Beta"},
        headers=auth_headers,
    ).json()

    add_resp = client.post(
        f"/projects/{project_one['id']}/members",
        json={"user_id": str(user.id), "role_in_project": "contributor"},
        headers=auth_headers,
    )
    assert add_resp.status_code == 201
    assert add_resp.json()["detail"] == "User added"

    user_list = client.get("/projects/", headers=user_headers)
    assert user_list.status_code == 200
    assert user_list.json()["total"] == 1
    assert user_list.json()["results"][0]["id"] == project_one["id"]

    allowed = client.get(f"/projects/{project_one['id']}", headers=user_headers)
    assert allowed.status_code == 200

    forbidden = client.get(f"/projects/{project_two['id']}", headers=user_headers)
    assert forbidden.status_code == 403
    assert forbidden.json()["detail"] == "Not authorized to view this project"


def test_list_and_remove_members(client, auth_headers, create_user, project_payload):
    member = create_user(
        {
            "user_id": "member-1",
            "name": "Member One",
            "email": "member1@example.com",
            "profile": "tester",
            "role": "user",
            "password": "secret123",
        }
    )

    project = client.post("/projects/", json=project_payload, headers=auth_headers).json()

    client.post(
        f"/projects/{project['id']}/members",
        json={"user_id": str(member.id), "role_in_project": "manager"},
        headers=auth_headers,
    )

    members_resp = client.get(f"/projects/{project['id']}/members", headers=auth_headers)
    assert members_resp.status_code == 200
    members_body = members_resp.json()
    assert members_body["total"] == 1
    assert members_body["results"][0]["user_id"] == str(member.id)
    assert members_body["results"][0]["role_in_project"] == "manager"

    remove_resp = client.delete(
        f"/projects/{project['id']}/members/{member.id}", headers=auth_headers
    )
    assert remove_resp.status_code == 200
    assert remove_resp.json()["detail"] == "User removed"

    members_after = client.get(f"/projects/{project['id']}/members", headers=auth_headers)
    assert members_after.json()["total"] == 0
