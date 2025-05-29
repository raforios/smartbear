'''
    Users Controller
'''
from typing import List
from datetime import datetime
from fastapi import Depends, HTTPException, status
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError
from models.users import User
from schemas.users import UserRequest, UserUpdateRequest, UserResponse
from services.security import verify_password, validate_token, hash_password

async def read_users(db) -> List[User] | None:
    '''
        Read All Users from Database
    '''
    users = db.query(User).all()
    if not users:
        return []
    return users

async def read_user(email: str, db) -> User | None:
    '''
        Read User by email from Database
    '''
    user = db.query(User).filter(User.email == email).first()

    if user is None:
        return None
    return user

async def create_user(user: UserRequest, db) -> User | None:
    '''
        Create a new user in the database with a hashed password.
    '''
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        return None

    db_user = User(**user.model_dump())
    hashed_password = hash_password(user.password)
    db_user.password = hashed_password
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

async def update_user(user: UserUpdateRequest, email: str, db) -> UserResponse | None:
    '''
        Update User
    '''
    db_user = db.query(User).filter(User.email == email).first()
    if db_user is None:
        return None

    if user.first_name is not None and isinstance(user.first_name, str):
        db_user.first_name = user.first_name
    if user.last_name is not None and isinstance(user.last_name, str):
        db_user.last_name = user.last_name
    if user.client is not None and isinstance(user.client, str):
        db_user.client = user.client
    if user.password is not None and isinstance(user.password, str):
        hashed_password = hash_password(user.password)
        db_user.password = hashed_password
    db_user.date_update = datetime.now()
    db_user.status = 1 if user.status == 1 else 0
    db.commit()
    db.refresh(db_user)
    user_response = UserResponse(
        email = db_user.email,
        first_name = db_user.first_name,
        last_name = db_user.last_name,
        client = db_user.client,
        role = db_user.role,
        status = db_user.status,
        date_register = db_user.date_register,
        date_update = db_user.date_update
    )

    return user_response

async def delete_user(email: str, db) -> User | None:
    '''
        Delete User
    '''
    db_user = db.query(User).filter(User.email == email).first()

    if db_user:
        db.delete(db_user)
        db.commit()
        return db_user

    return None


async def authenticate_user(email: str, password: str, db) -> User | None:
    '''
        Authenticate a user based on email and password.
    '''
    user = db.query(User).filter(User.email == email).first()
    if user and verify_password(password, user.password):
        return user
    return None

async def get_current_user(token: str, db) -> User | None:
    '''
        Current Users Controller
    '''
    credentials_exception = HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail = 'Could not validate credentials'
    )
    try:
        payload = validate_token(token)
        email: str = payload.get('sub')
        if email is None:
            raise ExpiredSignatureError
    except ExpiredSignatureError as exeception:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED,
                            detail = 'Expired Token') from exeception
    except InvalidTokenError as exeception:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN,
                            detail = 'Invalid Token') from exeception
    user = await read_user(email, db)

    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    '''
        Active Users
    '''
    if not current_user['status']:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = 'Inactive user')
    return current_user
