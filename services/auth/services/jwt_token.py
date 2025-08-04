'''
    JWT Service Provider
'''
import os
from datetime import datetime, timedelta, timezone
from typing import Dict, Any, Optional
from jose import jwt, JWTError

from dotenv import dotenv_values

from services.logger_config import custom_logger as logger
from services.exceptions import ServiceUnavailableError

_LOCAL_ENV_PARAMS = dotenv_values('.env') if os.path.exists('.env') else {}

# Secret key to signature JWT tokens
SECRET_KEY = os.environ.get('SECRET_KEY') or \
                      _LOCAL_ENV_PARAMS.get('SECRET_KEY')

if not SECRET_KEY:
    ERROR_MSG = 'SECRET_KEY is not configured in environment or .env.'
    logger.critical(ERROR_MSG)
    raise ServiceUnavailableError(
        detail = ERROR_MSG
    )

ALGORITHM = os.environ.get('ALGORITHM') or \
                      _LOCAL_ENV_PARAMS.get('ALGORITHM')

if not ALGORITHM:
    ERROR_MSG = 'ALGORITHM for JWT is not configured in environment or .env.'
    logger.critical(ERROR_MSG)
    raise ServiceUnavailableError(
        detail = ERROR_MSG
    )

ACCESS_TOKEN_EXPIRE_MINUTES = os.environ.get('ACCESS_TOKEN_EXPIRE_MINUTES') or \
                      _LOCAL_ENV_PARAMS.get('ACCESS_TOKEN_EXPIRE_MINUTES')

try:
    ACCESS_TOKEN_EXPIRE_MINUTES = int(ACCESS_TOKEN_EXPIRE_MINUTES)
except (TypeError, ValueError) as e:
    ERROR_MSG = '''ACCESS_TOKEN_EXPIRE_MINUTES is not configured or is not a
                valid integer in environment or .env.'''
    logger.critical(ERROR_MSG)
    raise ServiceUnavailableError(
        detail = ERROR_MSG
    ) from e

def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    '''
        Creates a JWT access token.
        data: Dictionary of data to include in the token (e.g., email, user_id).
        expires_delta: Optional, the token's lifetime. If not specified,
        use ACCESS_TOKEN_EXPIRE_MINUTES.
    '''
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes = int(ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({'exp': expire.timestamp()})

    try:
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm = ALGORITHM)
        message = f'JWT created for user: {data.get('email')}'
        logger.info(message)
        return encoded_jwt
    except Exception as e:
        error_msg = f'Error creating JWT token for user {data.get('email')}: {e}'
        logger.critical(error_msg)
        raise ServiceUnavailableError(
            detail = 'Failed to create authentication token.'
        ) from e

def decode_access_token(token: str) -> Optional[Dict[str, Any]]:
    '''
        Decodes and validates a JWT access token.
        Returns the token data if valid, None if not.
    '''
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms = [ALGORITHM])
        message = f'JWT decoded successfully. Payload email: {payload.get('email')}'
        logger.info(message)
        return payload
    except JWTError as e:
        message = f'Invalid JWT token: {e}'
        logger.warning(message)
        return None
