"""
FastAPI application entrypoint.
Exposes a user registration endpoint using the secure User model,
Pydantic schemas, and password hashing built in this module.
"""
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.database import get_db, Base, engine
from app.models.user import User
from app.models.calculation import Calculation
from app.schemas.user import UserCreate, UserRead
from app.security import hash_password

# Create tables on startup if they don't already exist.
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Secure User Model API")


@app.get("/")
def read_root():
    return {"message": "Secure User Model API is running"}


@app.post("/users/", response_model=UserRead, status_code=201)
def create_user(user_in: UserCreate, db: Session = Depends(get_db)):
    """Register a new user with a securely hashed password."""
    new_user = User(
        username=user_in.username,
        email=user_in.email,
        password_hash=hash_password(user_in.password),
    )
    db.add(new_user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Username or email already registered")
    db.refresh(new_user)
    return new_user


@app.get("/users/{user_id}", response_model=UserRead)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """Fetch a user by ID (password_hash is never returned, per UserRead schema)."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
