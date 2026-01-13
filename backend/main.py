from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello FastAPI"}

@app.get("/first")
def first():
    return {"message": "Hello FastAPI from first route"}

@app.get("/second")
def second():
    return {"message": "Hello FastAPI from second route"}