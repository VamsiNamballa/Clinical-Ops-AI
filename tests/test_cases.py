from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_patch_case_valid_status(test_case):
    response = client.patch(
        f"/cases/{test_case}",
        json={"status": "closed"},
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == test_case
    assert data["status"] == "closed"


def test_patch_case_not_found():
    response = client.patch(
        "/cases/999999",
        json={"status": "in_progress"},
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Case Not Found"}


def test_patch_case_invalid_status(test_case):
    response = client.patch(
        f"/cases/{test_case}",
        json={"status": "random_status"},
    )

    assert response.status_code == 422