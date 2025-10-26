from fastapi import FastAPI
from routers import auth, users
from database import Base, engine

app = FastAPI(title="Adviters POC", version="0.2.0")

@app.on_event("startup")
def on_startup():
    # Para POC; en prod usar Alembic
    Base.metadata.create_all(bind=engine)

@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
