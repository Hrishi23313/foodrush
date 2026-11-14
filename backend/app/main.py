from fastapi import FastAPI

app = FastAPI(
    title="FoodRush API",
    description="Multi-restaurant food ordering backend",
    version="0.1.0",
)


@app.get("/")
def read_root():
    return {"message": "Welcome to FoodRush API v1"}


@app.get("/health/db")
def health_check():
    return {"status": "ok"}