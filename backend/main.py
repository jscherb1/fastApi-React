from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root(name: str = "Guest"):
    return {"message": f"Hello World! Welcome {name}"}