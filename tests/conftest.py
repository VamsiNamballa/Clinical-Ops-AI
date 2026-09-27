import pytest

from app.db import get_connection

@pytest.fixture
def test_case():
    # Create Test Data
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO cases (patient_id,status)
                VALUES (%s,%s)
                RETURNING id;
                """
                ,
                ("TEST-PATIENT-001","open")
            )
            case_id=cur.fetchone()[0]
        conn.commit()
    
    # Give the Test ID that was actually created
    yield case_id

    # Clean up after the test
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "DELETE FROM cases WHERE id = %s;",
                (case_id,),
            )

        conn.commit()    
