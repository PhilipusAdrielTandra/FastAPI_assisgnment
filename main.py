from fastapi import FastAPI, Path
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

todos = {
    "a077953d-9e19-4ac3-9339-aec0e6b8f673": {
        "completed": False,
        "created": "May 3rd 2023",
        "text": "Do the dishes"
    }
}

class Todo(BaseModel):
    text: str
    completed: bool
    created: str

class UpdateTodo(BaseModel):
    text: Optional[str] = None
    completed : Optional[bool] = None
    created: Optional[str] = None

@app.get("/")
def index():
    return {"name": "First Data"}

@app.get("/get-todo/{todo_id}")
def get_todo(todo_id : str):
    return todos[todo_id]

@app.get("/get-by-todo/{todo_id}")
def get_todo(*, todo_id: str,text : Optional[str] = None, test: int):
    for todo_id in todos:
        if todos[todo_id]["text"] == text:
            return todos[todo_id]
    return {"Data": "Not Found"}

@app.post("/create-todo/{todo_id}")
def create_todo(todo_id : str, todo : Todo):
    if todo_id in todos:
        return {"Error": "Todo exists"}
    
    todos[todo_id] = todo
    return todos[todo_id]

@app.put("/update-student/{student_id}")
def update_todo(todo_id : str, todo: UpdateTodo):
    if todo_id not in todos:
        return {"Error": "Todo does not exist"}

    # if todo.text != None:
    #     todos[todo_id].text = todo.text

    # if todo.completed != None:
    #     todos[todo_id].text = todo.completed
    
    # if todo.created != None:
    #     todos[todo_id].text = todo.created

    todos[todo_id] = todo
    return todos[todo_id]

@app.delete("/delete-todo/{todo_id}")
def delete_todo(todo_id: str):
    if todo_id not in todos:
        return {"Error" : "Todo does not exist"}
    
    del todos[todo_id]
    return {"Message": "Todo deleted successfully"}