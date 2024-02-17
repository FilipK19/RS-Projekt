from fastapi import FastAPI, Request, HTTPException, Depends, status
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordBearer
from fastapi.templating import Jinja2Templates
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from passlib.context import CryptContext


app = FastAPI()
templates = Jinja2Templates(directory="templates")



MONGO_URI = "mongodb+srv://admin:admin123@cluster0.1cbo1.mongodb.net/"
DATABASE_NAME = "Userdata"
client = AsyncIOMotorClient(MONGO_URI)
db = client[DATABASE_NAME]

# Security configurations
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

# OAuth2 password bearer for authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")



@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("welcome.html", {"request": request})


@app.get("/home")
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


# User model for MongoDB
class User(BaseModel):
    username: str
    password: str

# Pydantic model for user registration
class UserCreate(User):
    pass

# Pydantic model for user login
class UserLogin(User):
    pass

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Function to verify password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Function to get user from MongoDB by username
async def get_user(username: str):
    user = await db.users.find_one({"username": username})
    return user

# Function to create a new user
async def create_user(user: UserCreate):
    user_dict = user.dict()
    user_dict["password"] = pwd_context.hash(user.password)
    result = await db.users.insert_one(user_dict)
    return user

# Function to authenticate user and get user data
async def authenticate_user(username: str, password: str):
    user = await get_user(username)
    if user and verify_password(password, user["password"]):
        return user

# Dependency to get current user
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401, detail="Invalid credentials", headers={"WWW-Authenticate": "Bearer"}
    )
    user = await get_user(token)
    if user is None:
        raise credentials_exception
    return user


@app.get("/register", response_class=HTMLResponse)
async def register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

# Route to create a new user
async def get_user_by_username(username: str):
    user = await db.users.find_one({"username": username})
    return user

@app.post("/register", response_model=User)
async def register(user: UserCreate):
    # Check if the username is already taken
    existing_user = await get_user_by_username(user.username)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already taken")

    # If username is not taken, create the user
    await create_user(user)
    
    return user


@app.post("/login")
async def login(user: UserLogin):
    user_data = await authenticate_user(user.username, user.password)
    if user_data is None:
        raise HTTPException(status_code=401, detail="Invalid credentials", headers={"WWW-Authenticate": "Bearer"})
    return {"access_token": user_data["username"], "token_type": "bearer"}

