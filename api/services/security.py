'''
    JWT Service Provider
'''
from datetime import datetime, timedelta, timezone
import jwt
from passlib.context import CryptContext
from dotenv import dotenv_values

PARAMETERS = dotenv_values('.env')
pwd_context = CryptContext(schemes = ['bcrypt'], deprecated = 'auto')

def verify_password(plain_password: str, hashed_password: str) -> bool | None:
    '''
        Verifying password
    '''
    return pwd_context.verify(plain_password, hashed_password)

def hash_password(password: str) -> str | None:
    ''' 
        Hashing password
    '''
    return pwd_context.hash(password)

def create_access_token(data: dict) -> str | None:
    '''
        Create JWT token for authentication
    '''
    to_encode = data.copy()
    expires_delta = timedelta(minutes = int(PARAMETERS['ACCESS_TOKEN_EXPIRE_MINUTES']))
    expire = datetime.now(timezone.utc) + expires_delta

    to_encode.update({'exp': expire})

    return jwt.encode(to_encode, PARAMETERS['SECRET_KEY'], algorithm = PARAMETERS['ALGORITHM'])

def validate_token(token: str) -> dict | None:
    '''
        Validate JWT token
    '''
    return jwt.decode(token, PARAMETERS['SECRET_KEY'], algorithms = PARAMETERS['ALGORITHM'])
