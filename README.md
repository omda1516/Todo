Here's an updated version of the `README.md` file that includes instructions for creating a virtual environment and installing the necessary libraries:

```markdown
# Todo API with FastAPI

This project is a Todo API built with FastAPI, allowing users to register accounts, log in, and manage their todo lists.

## Features

- User registration
- User login and access token generation
- Create, read, update, and delete todo items
- Protected endpoints using OAuth2

## Requirements

- Python 3.12.6

## Installation

To install the project, follow these steps:

1. **Create a Virtual Environment:**

   ```bash
   python -m venv venv
   ```

2. **Activate the Virtual Environment:**
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

3. **Clone the Repository:**
   ```bash
   git clone https://github.com/omda1516/Todo.git
   ```

4. **Navigate to the Project Folder:**
   ```bash
   cd Todo
   ```

5. **Install the Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

To run the application, use the following command:
```bash
uvicorn main:app --reload
```

You can access the interactive API documentation (Swagger UI) at:
```
http://127.0.0.1:8000/docs
```

## Endpoints

- **User Registration:**
  - `POST /register/`
  
- **User Login:**
  - `POST /token`
  
- **Create a New Todo Item:**
  - `POST /todos/`
  
- **Read All Todo Items:**
  - `GET /todos/`
  
- **Read a Specific Todo Item:**
  - `GET /todos/{todo_id}`
  
- **Update a Specific Todo Item:**
  - `PUT /todos/{todo_id}`
  
- **Delete a Specific Todo Item:**
  - `DELETE /todos/{todo_id}`

## Demo

A demo of the application is available in the following video:
- todo.mp4

## Postman Collection

You can import the Postman collection to test the API endpoints:
- Todo.postman_collection.json



