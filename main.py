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


SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("welcome.html", {"request": request})


@app.get("/home")
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


class User(BaseModel):
    username: str
    password: str

class UserCreate(User):
    pass

class UserLogin(User):
    pass

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

async def get_user(username: str):
    user = await db.users.find_one({"username": username})
    return user

async def create_user(user: UserCreate):
    user_dict = user.dict()
    user_dict["password"] = pwd_context.hash(user.password)
    result = await db.users.insert_one(user_dict)
    return user

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

async def get_user_by_username(username: str):
    user = await db.users.find_one({"username": username})
    return user

@app.post("/register", response_model=User)
async def register(user: UserCreate):
    existing_user = await get_user_by_username(user.username)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already taken")
    await create_user(user)
    return user

@app.post("/login")
async def login(user: UserLogin):
    user_data = await authenticate_user(user.username, user.password)
    if user_data is None:
        raise HTTPException(status_code=401, detail="Invalid credentials", headers={"WWW-Authenticate": "Bearer"})
    return {"access_token": user_data["username"], "token_type": "bearer"}

