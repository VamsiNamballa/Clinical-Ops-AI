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


def test_create_and_get_case(case_cleanup):
    # Create a case through the API.
    create_response = client.post(
        "/cases",
        json={
            "patient_id": "TEST-POST-001",
            "status": "open",
        },
    )

    assert create_response.status_code == 200

    created_case = create_response.json()
    case_id = created_case["id"]

    # Register the created case for cleanup.
    case_cleanup.append(case_id)

    assert created_case["patient_id"] == "TEST-POST-001"
    assert created_case["status"] == "open"

    # Retrieve the same case through the API.
    get_response = client.get(f"/cases/{case_id}")

    assert get_response.status_code == 200

    retrieved_case = get_response.json()

    assert retrieved_case["id"] == case_id
    assert retrieved_case["patient_id"] == "TEST-POST-001"
    assert retrieved_case["status"] == "open"
    
def test_get_cases_contains_created_case(case_cleanup):
    create_response = client.post(
        "/cases",
        json={
            "patient_id": "TEST-LIST-001",
            "status": "open",
        },
    )

    assert create_response.status_code == 200

    created_case = create_response.json()
    case_id = created_case["id"]

    case_cleanup.append(case_id)

    response = client.get("/cases")

    assert response.status_code == 200

    cases = response.json()

    assert isinstance(cases, list)

    matching_cases = [
        case
        for case in cases
        if case["id"] == case_id
    ]

    assert len(matching_cases) == 1
    assert matching_cases[0]["patient_id"] == "TEST-LIST-001"
    assert matching_cases[0]["status"] == "open"