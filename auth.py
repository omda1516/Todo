from datetime import timedelta, datetime
from typing import Optional
from fastapi.security import OAuth2PasswordBearer
import jwt
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
SECRET_KEY = "your_secret_key"  
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Function to verify if the provided password matches the hashed password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Function to hash a password
def get_password_hash(password):
    return pwd_context.hash(password)

# Function to retrieve a user from the database by username
async def get_user(db, username: str):
    user = db.find_one({"username": username})  
    return user

# Function to create a new access token
async def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()  
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)  
    to_encode.update({"exp": expire})  
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
