from typing import List, Optional
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
import uvicorn

class TodoList(BaseModel):
    id: int
    title: str
    description: str


app = FastAPI()
todo: List[TodoList] = []

@app.get("/", response_model=List[TodoList], status_code=status.HTTP_200_OK)
def get_todo_list():
    return todo

@app.post("/", response_model=TodoList, status_code=status.HTTP_201_CREATED)
async def create_todo_list(todo_item: TodoList):
    todo.append(todo_item)
    return todo_item

@app.get("/{todo_id}")
async def get_todo_by_id(todo_id: int):
    for item in todo:
        if item.id == todo_id:
            return item
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")

@app.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(todo_id: int):
    todo_item = next((item for item in todo if item.id == todo_id))
    if not todo_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    todo.remove(todo_item)

@app.post("/update/{todo_id}", response_model=TodoList, status_code=status.HTTP_200_OK)
async def update_todo(todo_id: int, todo_item: TodoList):
    for i, item in enumerate(todo):
        if item.id == todo_id:
            todo[i] = todo_item
            return todo_item
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
