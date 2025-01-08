
from pymongo import MongoClient
from pymongo.server_api import ServerApi


uri = "mongodb+srv://zaherkryem:zaher1234@todo.p91ej.mongodb.net/?retryWrites=true&w=majority&appName=todo"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client.todo_db
todo_collection = db["todos"]
user_collection = db["users"]