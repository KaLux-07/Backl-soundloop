from fastapi import FastAPI, HTTPException, status, Depends, UploadFile, File, Form
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
import os

import logging

from funciones import *
from fastapi.middleware.cors import CORSMiddleware
from models.User import User
from models.Loop import Loop
from models.SoundLoop import SoundLoop
from models.Sound import Sound

logging.basicConfig(level=logging.INFO)

SECRET_KEY = os.urandom(32)
SECRET_KEY_HEX = SECRET_KEY.hex()

app = FastAPI()

SECRET_KEY = SECRET_KEY_HEX
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_SECONDS = 10
ACCESS_TOKEN_EXPIRE_MINUTES = 10
ACCESS_TOKEN_EXPIRE_DAYS = 1


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# username and password verification / Implementation of JWT
def verify_password(password, password_hash):
    return pwd_context.verify(password, password_hash)

def get_user(username):
    connection = connect_to_database()
    result = get_all_users(connection)
    close_connection(connection)

    for user in result:
        if user["username"] == username:
            return user

    return False

def authenticate_user(username, password):
    user = get_user(username)
    if not user:
        return False
    if not verify_password(password, user['password_hash']):
        return False

    return user

def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.now() + expires_delta
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

@app.post('/token', tags=['token'])
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username or password is not valid",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    access_token_expires = timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
    access_token = create_access_token(
        data={'sub': user['username']},
        expires_delta=access_token_expires
    )

    return {'access_token': access_token, 'token_type': 'bearer'}

@app.get("/token/data", tags=['token'])
async def read_users_me(token: str = Depends(OAuth2PasswordBearer(tokenUrl="/token"))):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=403, detail="Se requiere autenticación")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido")
    
    user = get_user(username)
    if user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"username": user["username"], "id": user["id"]}

# Requests for Users
@app.get('/users', tags=['users'])
async def get_users():
    connection = connect_to_database()
    result = get_all_users(connection)
    close_connection(connection)
    return result

@app.get('/users/{userId}', tags=['users'])
async def get_user_by_id(userId):
    connection = connect_to_database()
    result = get_user_by_user_id(connection, userId)
    close_connection(connection)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    
    return result

@app.post('/users', tags=['users'])
async def create_user(userData: User):
    password = userData.password_hash
    password_hash = pwd_context.hash(password)
    userData.password_hash = password_hash

    connection = connect_to_database()
    insert_ok = insert_user(connection, userData)
    
    if not insert_ok:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Cannot create user')

    close_connection(connection)

    return {'status': status.HTTP_200_OK, 'message': 'User created successfully'}

@app.delete('/users', tags=['users'])
def delete_user(user_id):
    connection = connect_to_database()
    deleteOk = delete_user_by_id(connection, user_id)
    close_connection(connection)

    if not deleteOk:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Cannot delete user')
    
    return {'status': status.HTTP_200_OK, 'message': 'User delete successfully'}

# Requests for soundloops 
@app.get('/user/{user_id}/soundloops', tags=['soundloops'])
def get_user_soundLoops(user_id):
    connection = connect_to_database()
    result = get_soundLoops(connection, user_id)
    close_connection(connection)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='SoundLoop not found')
    
    return result

@app.get('/user/{user_id}/soundloop/{loop_id}', tags=['soundloops'])
def get_user_soundLoop_by_id(user_id, loop_id):
    connection = connect_to_database()
    result = get_soundLoop_by_id(connection, loop_id, user_id)
    close_connection(connection)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='SoundLoop not found')
    
    return result

@app.post('/user/soundloop/', tags=['soundloops'])
def create_soundLoop(loopData: Loop):
    connection = connect_to_database()
    insertOk = insert_soundloop(connection, loopData.loop_name, loopData.user_id)

    if not insertOk:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Cannot create soundloop')

    close_connection(connection)

    return {'status': status.HTTP_200_OK, 'message': 'SoundLoop created successfully'}

@app.delete('/user/soundloop/{loop_id}', tags=['soundloops'])
def delete_loop(loop_id):
    connection = connect_to_database()
    deleteOk = delete_soundLoop(connection, loop_id)
    close_connection(connection)

    if not deleteOk:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Cannot delete soundloop')
    
    return {'status': status.HTTP_200_OK, 'message': 'SoundLoop delete successfully'}

@app.put('/user/soundloop/', tags=['soundloops'])
def update_soundLoop(sound_loop_data: SoundLoop):
    connection = connect_to_database()
    insertOk = update_soundLoop_name(connection, sound_loop_data)

    if not insertOk:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Cannot update soundloop name')

    close_connection(connection)

    return {'status': status.HTTP_200_OK, 'message': 'SoundLoop name updated successfully'}

# Request for sounds
@app.get('/user/{user_id}/soundloop/{loop_id}/sounds', tags=['sounds'])
def get_sounds(user_id, loop_id):
    connection = connect_to_database()
    result = get_sound(connection, loop_id, user_id)
    close_connection(connection)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Sounds not found')
    
    return result

@app.post('/user/soundloop/sounds', tags=['sounds'])
def insert_sounds(blob: UploadFile = File(...), user_id: int = Form(...), loop_id: int = Form(...)):
    blob_content = blob.file.read()

    connection = connect_to_database()
    insertOk = insert_sound(connection, blob_content, user_id, loop_id)
    close_connection(connection)

    if not insertOk:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Cannot create the sounds')

    return {'status': status.HTTP_200_OK, 'message': 'Sounds created successfully'}

@app.delete('/user/{user_id}/soundloop/{loop_id}/sounds', tags=['sounds'])
def delete_sounds(user_id, loop_id):
    connection = connect_to_database()
    deleteOk = delete_sound_from_template(connection, user_id, loop_id)
    close_connection(connection)

    if not deleteOk:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Cannot delete sounds')
    
    return {'status': status.HTTP_200_OK, 'message': 'Sounds delete successfully'}



    

