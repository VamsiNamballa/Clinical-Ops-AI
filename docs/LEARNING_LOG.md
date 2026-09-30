# Clinical Ops AI — Learning Log

## 2026-09-27

### REST API — PATCH vs PUT

I learned that PATCH is appropriate for a partial resource update. In the case API, PATCH changes only the case status without replacing the entire case representation.

### FastAPI / Pydantic Validation

`CaseUpdate` restricts status using `Literal` to:

- `open`
- `in_progress`
- `closed`

FastAPI/Pydantic validates the request before the endpoint executes. An invalid value such as `random_status` therefore returns HTTP 422 before the PostgreSQL UPDATE statement runs.

### Automated Testing

Verified with:

`python -m pytest -v`

Result: 5 passed, 1 dependency deprecation warning.

The tests cover:

- valid case status update
- nonexistent case returning HTTP 404
- invalid status returning HTTP 422
- create case and retrieve the same persisted record
- list cases and confirm the created case appears
