# Clinical Ops AI — Progress

## Backend Foundation

- FastAPI application created.
- `GET /health` implemented and verified.
- PostgreSQL database and application user configured.
- Python-to-PostgreSQL connectivity verified.
- Reusable Psycopg database connection helper implemented.
- `GET /db-health` implemented and verified end-to-end.

## Case API

- `POST /cases` implemented and verified with PostgreSQL persistence.
- `GET /cases/{case_id}` implemented and verified.
- Missing case retrieval returns HTTP 404.
- `GET /cases` implemented and verified.
- `PATCH /cases/{case_id}` implemented and verified.
- Missing case updates return HTTP 404.
- Case status restricted to `open`, `in_progress`, or `closed`.
- Invalid case status is rejected with HTTP 422.

## Automated Testing

- pytest configured in the project virtual environment.
- FastAPI endpoints tested using `TestClient`.
- Automated PATCH test covers a valid status update.
- Automated PATCH test covers a nonexistent case returning HTTP 404.
- Automated PATCH test covers an invalid status returning HTTP 422.
- `test_case` pytest fixture creates test data before dependent tests.
- Fixture yields the generated case ID instead of relying on a hard-coded database ID.
- Fixture deletes its test case after the test completes.
- Latest verification: `python -m pytest -v` -> 5 passed, 1 dependency deprecation warning.
- Automated POST + GET test creates a case and retrieves the same persisted record.
- Automated GET /cases test verifies that a newly created case appears in the collection response.

## Current Scope

Implemented and verified:
- FastAPI backend foundation.
- PostgreSQL connectivity and persistence.
- Basic case create, read, list, and status-update operations.
- Request validation and HTTP error handling.
- Initial automated API regression tests with isolated test data.

Not yet implemented:
- Delete case endpoint.
- Additional automated coverage for edge cases and future endpoints.
- Docker containerization.
- RAG pipeline and vector retrieval.
- Microsoft Foundry integration.
- LLM/agent functionality.
- Authentication and authorization.
- Frontend application.
