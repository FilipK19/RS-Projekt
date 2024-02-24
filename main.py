from fastapi import Depends, FastAPI, HTTPException, status,  Request, Cookie, Response
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from typing import Annotated
from fastapi.security.base import SecurityBase


app = FastAPI()
templates = Jinja2Templates(directory="templates")

#Detalji za token
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

#MongoDB baza
MONGO_URI = "mongodb+srv://admin:admin123@cluster0.1cbo1.mongodb.net/"
DB_NAME = "ztest"
client = AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]


#Basemodel za Mongo
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

class User(BaseModel):
    username: str

class UserInDB(User):
    hashed_password: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


#Pomocne funkcije
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

async def get_user(db, username: str):
    user_dict = await db.users.find_one({"username": username})
    if user_dict:
        return UserInDB(**user_dict)

async def authenticate_user(username: str, password: str):
    user = await get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

class CookieToken(SecurityBase):
    def __call__(self, request: Request):
        return request.cookies.get("token")

async def getuser(token: str = Depends(CookieToken())):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = await get_user(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def create_user(db, user: UserInDB):
    await db.users.insert_one(user.dict())


#Post rute
@app.post("/register/", response_model=User)
async def create_user_endpoint(user: UserInDB):
    existing_user = await get_user(db, username=user.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    
    hashed_password = get_password_hash(user.hashed_password)
    user_data = user.dict()
    user_data["hashed_password"] = hashed_password

    await create_user(db, UserInDB(**user_data))

    return user

@app.post("/token")
async def login_for_access_token(response: Response,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    response.set_cookie(key="token", value=access_token, httponly=True)
    return Token(access_token=access_token, token_type="bearer")


#Get rute
@app.get("/register", response_class=HTMLResponse)
async def register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.get("/test", response_class=HTMLResponse)
def protected_route(request: Request, current_user: User = Depends(getuser)):
    return templates.TemplateResponse("test.html", {"request": request, "username": current_user.username})

@app.get("/home")
async def home(request: Request, current_user: User = Depends(getuser)):
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("welcome.html", {"request": request})