'''
    Auth: route handlers
'''
from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import APIRouter, status, Depends, HTTPException
from schemas.auth import LoginRequest, SignupResponse, Token
from schemas.users import UserRequest
from services.database import get_db
from services.security import create_access_token
from services.logger_config import custom_logger as logger
from controllers.users import authenticate_user, create_user

router = APIRouter(prefix = '/api/v1', tags = ['Authentication'])
DB = Annotated[Session, Depends(get_db)]

@router.post('/login', response_model = Token, status_code = status.HTTP_202_ACCEPTED)
async def login(request: LoginRequest, db: DB):
    '''
        Login route for obtaining an access token after verifying credentials.
    '''
    user = await authenticate_user(request.email, request.password, db)
    if not user:
        logger.error('Invalid credentials: %s', request.email)
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED,
                            detail = 'Invalid credentials')

    # Generate an access token
    access_token = create_access_token({'sub': user.email})
    logger.info('User %s started session', user.email)
    return Token(access_token = access_token, token_type = 'bearer')

@router.post('/signup', response_model = SignupResponse, status_code = status.HTTP_201_CREATED)
async def signup(user: UserRequest, db: DB):
    '''
        Sign-up route for creating a new user and storing their credentials securely.
    '''
    # Create the new user
    db_user = await create_user(user, db)
    if db_user is None:
        logger.error('Email already registered %s', user.email)
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST,
                            detail = 'Email already registered')

    logger.info('User %s created successfully', user.email)
    return SignupResponse(user_email = db_user.email,
                        message = 'User created successfully')
