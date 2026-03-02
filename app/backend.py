from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import uvicorn

app = FastAPI(title="Todo API")

# Allow CORS for the frontend (running on any origin for simplicity)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TodoBase(BaseModel):
    title: str
    description: str | None = None
    completed: bool = False

class TodoCreate(TodoBase):
    pass

class Todo(TodoBase):
    id: int

# In-memory storage (replace with a DB for production)
_todos: List[Todo] = []
_next_id = 1

@app.get("/todos", response_model=List[Todo])
def list_todos():
    return _todos

@app.post("/todos", response_model=Todo, status_code=201)
def create_todo(todo: TodoCreate):
    global _next_id
    new_todo = Todo(id=_next_id, **todo.dict())
    _todos.append(new_todo)
    _next_id += 1
    return new_todo

@app.get("/todos/{todo_id}", response_model=Todo)
def get_todo(todo_id: int):
    for t in _todos:
        if t.id == todo_id:
            return t
    raise HTTPException(status_code=404, detail="Todo not found")

@app.put("/todos/{todo_id}", response_model=Todo)
def update_todo(todo_id: int, todo: TodoCreate):
    for idx, t in enumerate(_todos):
        if t.id == todo_id:
            updated = Todo(id=todo_id, **todo.dict())
            _todos[idx] = updated
            return updated
    raise HTTPException(status_code=404, detail="Todo not found")

@app.delete("/todos/{todo_id}", status_code=204)
def delete_todo(todo_id: int):
    for idx, t in enumerate(_todos):
        if t.id == todo_id:
            _todos.pop(idx)
            return
    raise HTTPException(status_code=404, detail="Todo not found")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)