from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from database import user_collection, todo_collection
from models import User, TodoItem, Token,Todo
from auth import (
    get_user, get_password_hash,
    create_access_token, verify_password,
    oauth2_scheme,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    SECRET_KEY,
    ALGORITHM
)
from bson.objectid import ObjectId
from datetime import timedelta
import jwt

app = FastAPI()

# Endpoint for user registration
@app.post("/register/")
async def register(user: User):

    existing_user = await get_user(user_collection, user.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
 
    hashed_password = get_password_hash(user.password)
    user_data = user.dict()
    user_data["password"] = hashed_password  
    user_collection.insert_one(user_data) 
    return {"msg": "User registered successfully"}

# Endpoint for user login and token generation
@app.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):

    user = await get_user(user_collection, form_data.username)
    if not user or not verify_password(form_data.password, user["password"]):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    
    # Create access token with expiration
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = await create_access_token(data={"sub": user["username"]}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

# Endpoint to create a new todo item
@app.post("/todos/", response_model=Todo)
async def create_todo(item: Todo, token: str = Depends(oauth2_scheme)):
    username = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])["sub"]
    item_dict = item.dict()
    item_dict["owner"] = username  
    result = todo_collection.insert_one(item_dict) 
    item_dict["id"] = str(result.inserted_id)  
    return item_dict

# Endpoint to read all todo items for the authenticated user
@app.get("/todos/")
async def read_todos(token: str = Depends(oauth2_scheme)):
    username = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])["sub"]
    todos = []
    for todo in todo_collection.find({"owner": username}):
        todo["_id"] = str(todo["_id"])  
        todo["id"] = todo["_id"] 
        todos.append(todo)
    return todos

# Endpoint to read a specific todo item by ID
@app.get("/todos/{todo_id}", response_model=TodoItem)
async def read_todo(todo_id: str, token: str = Depends(oauth2_scheme)):
    username = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])["sub"]
    todo = todo_collection.find_one({"_id": ObjectId(todo_id), "owner": username})
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    todo["_id"] = str(todo["_id"])  
    todo["id"] = todo["_id"]  
    return todo

# Endpoint to update a specific todo item
@app.put("/todos/{todo_id}", response_model=Todo)
async def update_todo(todo_id: str, item: Todo, token: str = Depends(oauth2_scheme)):
    username = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])["sub"]
    existing_todo = todo_collection.find_one({"_id": ObjectId(todo_id), "owner": username})
    if not existing_todo:
        raise HTTPException(status_code=404, detail="Todo not found or not owned by user")
    
    # Update the todo item while excluding the owner field
    result = todo_collection.update_one(
        {"_id": ObjectId(todo_id), "owner": username}, 
        {"$set": item.dict(exclude_unset=True, exclude={"owner"})}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=400, detail="No changes made to the Todo")
    
    updated_todo = todo_collection.find_one({"_id": ObjectId(todo_id)})
    
    return {
        "title": updated_todo["title"],
        "description": updated_todo["description"],
        "status": updated_todo["status"],
        "due_date": updated_todo["due_date"],
        "owner": existing_todo["owner"], 
        "id": str(updated_todo["_id"])
    }

# Endpoint to delete a specific todo item
@app.delete("/todos/{todo_id}")
async def delete_todo(todo_id: str, token: str = Depends(oauth2_scheme)):
    username = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])["sub"]
    result = todo_collection.delete_one({"_id": ObjectId(todo_id), "owner": username})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Todo not found or not owned by user")
    return {"msg": "Todo deleted successfully"}
