from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException
import models
from models import Todos
from database import engine, SessionLocal
app = FastAPI()

models.Base.metadata.create_all(bind=engine)
def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
@app.get("/")
async def read_all(db: db_dependency):
    return db.query(Todos).all()


@app.get("/todo/{todo_id}")
async def read_by_id(db: db_dependency, todo_id: int):
    data = db.query(Todos).filter(Todos.id == todo_id).first()

    if data is not None:
        return data

    return HTTPException(status_code=404, detail="database not found")

