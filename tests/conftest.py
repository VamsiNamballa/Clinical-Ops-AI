import pytest

from app.db import get_connection


@pytest.fixture
def test_case():
    # Create test data directly in PostgreSQL.
    # Used when a test requires a case to already exist.
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO cases (patient_id, status)
                VALUES (%s, %s)
                RETURNING id;
                """,
                ("TEST-PATIENT-001", "open"),
            )
            case_id = cur.fetchone()[0]

        conn.commit()

    yield case_id

    # Clean up after the test.
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "DELETE FROM cases WHERE id = %s;",
                (case_id,),
            )

        conn.commit()


@pytest.fixture
def case_cleanup():
    # Store IDs created through the API during a test.
    case_ids = []

    yield case_ids

    # Clean up those cases after the test finishes.
    with get_connection() as conn:
        with conn.cursor() as cur:
            for case_id in case_ids:
                cur.execute(
                    "DELETE FROM cases WHERE id = %s;",
                    (case_id,),
                )

        conn.commit()