from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import HTTPException
from typing import Literal


from app.db import get_connection

# The Root
app=FastAPI(title="Clinical Ops AI")

# We Define Classes here
#Using the below class, we create new cases
class CaseCreate(BaseModel):
    patient_id: str
    status: str
    
#Using the Below class, we update Existing cases
class CaseUpdate(BaseModel):
    status: Literal["open", "in_progress", "closed"]


# Classes are Created before this

# From Here, the Get Check points Starts
# Root One
@app.get("/")
def hello():
    return ("Hello")

# HEalth Check 
# This end point checks if the FastAPI is running
# This runs even if PostGreSQL Server is down
@app.get("/health")
def health_check():
    return {"status":"ok"}

# This End point goes  step further by examining whether the FastAPI can connect to PGSQL
# and also run SQL Commands there
@app.get("/db-health")
def db_health():
    with get_connection() as conn:
        with conn.cursor() as cor:
            cor.execute("Select 1;")
            result=cor.fetchone()
    
    return {
         "database": "ok",
         "result": result[0]
    }

## This GET end points helps us with an SQL Query that 
## fetches all the details based on the given case id
@app.get("/cases/{case_id}")
def get_case(case_id:int):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, patient_id, status, created_at
                FROM cases
                WHERE id=%s
                """,
                (case_id,)
            )
            
            row=cur.fetchone()
            
    if row is None:
        raise HTTPException(status_code=404, detail="Case Not Found")
    
    return{
        "id":row[0],
        "patient_id":row[1],
        "status":row[2],
        "created_at":row[3]
    }

## This GET endpoint uses an SQL query that fetches 
## All the available cases 
@app.get("/cases")
def get_cases():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, patient_id, status, created_at
                FROM cases
                ORDER BY id;
                """   
            )
            rows=cur.fetchall()
    return [
        {
            "id":row[0],
            "patient_id":row[1],
            "status":row[2],
            "created_at":row[3]
        }
        for row in rows
    ]
  
# The Get Check points Ends here

# The POST Checkpoints starts here 

## The below POST end point runs an SQL query that 
## creates a new Case dynamically
@app.post("/cases")
def create_case(case: CaseCreate):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO cases (patient_id, status)
                VALUES (%s, %s)
                RETURNING id, patient_id, status, created_at;
                """,
                (case.patient_id, case.status)
            )

            row = cur.fetchone()

    return {
        "id": row[0],
        "patient_id": row[1],
        "status": row[2],
        "created_at": row[3]
    }
    
# The POST End points ends here

# Start of PATCH End Points

## The below PATCH end point helps us update the available case and its details
@app.patch("/cases/{case_id}")
def update_case(case_id:int, case: CaseUpdate):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE cases
                SET status=%s
                WHERE id=%s
                RETURNING id, patient_id, status, created_at;
                """,
                (case.status, case_id)
            )
            row=cur.fetchone()
    
    if row is None:
        raise HTTPException(status_code=404, detail="Case Not Found")
    
    return {
        "id":row[0],
        "patient_id":row[1],
        "status":row[2],
        "created_at": row[3]
    }
    
@app.delete("/cases/{case_id}")
def delete_case(case_id: int):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                DELETE FROM cases
                WHERE id=%s
                RETURNING id;
                """,
                (case_id,)
            )

            row = cur.fetchone()

    if row is None:
        raise HTTPException(
            status_code=404,
            detail="Case Not Found"
        )

    return {
        "message": "Case Deleted",
        "id": row[0]
    }
# End of Patch End Points