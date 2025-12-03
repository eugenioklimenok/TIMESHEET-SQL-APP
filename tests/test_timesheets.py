from datetime import date

import pytest


@pytest.fixture
def timesheet_payload():
    return {"period_start": "2024-01-01", "period_end": "2024-01-07"}


def _get_user_id_by_email(client, admin_headers, email):
    users_resp = client.get("/users/", headers=admin_headers)
    assert users_resp.status_code == 200
    for user in users_resp.json():
        if user["email"] == email:
            return user["id"]
    pytest.fail("User not found")


def _create_project_for_user(client, admin_headers, user_id):
    project_payload = {
        "code": "TS-PROJ",
        "name": "Timesheet Project",
        "description": "Project for timesheet tests",
        "client_name": "Client QA",
        "is_active": True,
    }
    project = client.post("/projects/", json=project_payload, headers=admin_headers)
    assert project.status_code == 201
    project_data = project.json()

    add_member = client.post(
        f"/projects/{project_data['id']}/members",
        json={"user_id": user_id, "role_in_project": "contributor"},
        headers=admin_headers,
    )
    assert add_member.status_code == 201
    return project_data


def test_user_can_submit_own_timesheet(client, user_headers, timesheet_payload):
    draft_resp = client.post("/timesheets/", json=timesheet_payload, headers=user_headers)
    assert draft_resp.status_code == 201
    timesheet = draft_resp.json()

    submit_resp = client.post(f"/timesheets/{timesheet['id']}/submit", headers=user_headers)
    assert submit_resp.status_code == 200
    body = submit_resp.json()
    assert body["success"] is True
    assert body["timesheet"]["status"] == "Submitted"
    assert body["timesheet"]["owner"] == timesheet["user_id"]


def test_admin_cannot_submit_others_timesheets(client, auth_headers, user_headers, timesheet_payload):
    draft_resp = client.post("/timesheets/", json=timesheet_payload, headers=user_headers)
    timesheet = draft_resp.json()

    submit_resp = client.post(f"/timesheets/{timesheet['id']}/submit", headers=auth_headers)
    assert submit_resp.status_code == 403
    error = submit_resp.json()
    assert error["success"] is False
    assert error["error"]["code"] == 403


def test_admin_can_approve_submitted_timesheet(client, auth_headers, user_headers, timesheet_payload):
    draft_resp = client.post("/timesheets/", json=timesheet_payload, headers=user_headers)
    timesheet = draft_resp.json()
    client.post(f"/timesheets/{timesheet['id']}/submit", headers=user_headers)

    approve_resp = client.post(f"/timesheets/{timesheet['id']}/approve", headers=auth_headers)
    assert approve_resp.status_code == 200
    body = approve_resp.json()
    assert body["success"] is True
    assert body["timesheet"]["status"] == "Approved"


def test_cannot_modify_items_after_submission(
    client, auth_headers, user_headers, user_payload, timesheet_payload
):
    owner_id = _get_user_id_by_email(client, auth_headers, user_payload["email"])
    project = _create_project_for_user(client, auth_headers, owner_id)

    draft_resp = client.post("/timesheets/", json=timesheet_payload, headers=user_headers)
    timesheet = draft_resp.json()

    create_item_resp = client.post(
        f"/timesheets/{timesheet['id']}/items",
        headers=user_headers,
        json={
            "project_id": project["id"],
            "date": date.fromisoformat(timesheet_payload["period_start"]).isoformat(),
            "description": "Initial work",
            "hours": 4,
        },
    )
    assert create_item_resp.status_code == 201

    client.post(f"/timesheets/{timesheet['id']}/submit", headers=user_headers)

    blocked_resp = client.post(
        f"/timesheets/{timesheet['id']}/items",
        headers=user_headers,
        json={
            "project_id": project["id"],
            "date": date.fromisoformat(timesheet_payload["period_start"]).isoformat(),
            "description": "Extra work",
            "hours": 2,
        },
    )
    assert blocked_resp.status_code == 400
    assert "Solo puedes modificar" in blocked_resp.json()["detail"]


def test_rejecting_submitted_timesheet(client, auth_headers, user_headers, timesheet_payload):
    draft_resp = client.post("/timesheets/", json=timesheet_payload, headers=user_headers)
    timesheet = draft_resp.json()
    client.post(f"/timesheets/{timesheet['id']}/submit", headers=user_headers)

    reject_resp = client.post(f"/timesheets/{timesheet['id']}/reject", headers=auth_headers)
    assert reject_resp.status_code == 200
    body = reject_resp.json()
    assert body["success"] is True
    assert body["timesheet"]["status"] == "Rejected"

    approve_after = client.post(f"/timesheets/{timesheet['id']}/approve", headers=auth_headers)
    assert approve_after.status_code == 409
    conflict = approve_after.json()
    assert conflict["success"] is False
    assert conflict["error"]["code"] == 409
