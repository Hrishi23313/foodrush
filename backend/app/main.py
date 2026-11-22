from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.database import get_db
from app.routes import auth, restaurants

app = FastAPI(
    title="FoodRush API",
    description="Multi-restaurant food ordering backend",
    version="0.1.0",
)

app.include_router(auth.router)
app.include_router(restaurants.router)


@app.get("/")
def read_root():
    return {"message": "Welcome to FoodRush API"}


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/health/db")
def database_health_check(db: Session = Depends(get_db)):
    result = db.execute(text("SELECT DATABASE()")).scalar()
    return {"status": "ok", "connected_to": result}