from fastapi import FastAPI, Path, Depends
from typing import Optional
from pydantic import BaseModel
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

TODOS = []

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

class Todo(BaseModel):
    text: str
    completed: bool
    created: str

@app.get("/")
def index(db: Session = Depends(get_db)):
    return db.query(models.Todos).all()

@app.get("/get-todo/{todo_id}")
def get_todo(todo_id : int, db: Session = Depends(get_db)):
    todo_model = db.query(models.Todos).filter(models.Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(
            status_code = 404,
            detail = f"ID {todo_id}: Does not exist"
        )
    return todo_model

@app.post("/")
def create_todo(todo : Todo, db: Session = Depends(get_db)):
    todo_model = models.Todos()
    todo_model.completed = todo.completed
    todo_model.created = todo.created
    todo_model.text = todo.text

    db.add(todo_model)
    db.commit()
    return todo

@app.put("/update-todo/{todo_id}")
def update_todo(todo_id : int, todo: Todo, db: Session = Depends(get_db)):
    todo_model = db.query(models.Todos).filter(models.Todos.id == todo_id).first()

    if todo_model is None:
        raise HTTPException(
            status_code = 404,
            detail = f"ID {todo_id}: Does not exist"
        )
    todo_model.completed = todo.completed
    todo_model.created = todo.created
    todo_model.text = todo.text

    db.add(todo_model)
    db.commit()
    return todo

@app.delete("/delete-todo/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    todo_model = db.query(models.Todos).filter(models.Todos.id == todo_id).first()
    
    if todo_model is None:
            raise HTTPException(
            status_code = 404,
            detail = f"ID {todo_id}: Does not exist"
        )
    
    db.query(models.Todos).filter(models.Todos.id == todo_id).delete()
    db.commit()
