from fastapi import FastAPI

app=FastAPI(title="Clinical Ops AI")

@app.get("/")
def hello():
    return ("Hello")

@app.get("/health")
def health_check():
    return {"status":"ok"}