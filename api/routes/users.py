'''
    Users: route handlers
'''
from typing import Annotated, Dict
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from controllers.auth import BearerToken
from controllers.users import update_user, delete_user
from schemas.users import UserUpdateRequest, UserResponse
from services.database import get_db
from services.logger_config import custom_logger as logger

router = APIRouter(prefix = '/api/v1/users', tags = ['Users'])
DB = Annotated[Session, Depends(get_db)]

@router.patch('/{email}', status_code = status.HTTP_200_OK,
            dependencies = [Depends(BearerToken())])
async def patch_user(email: str, user: UserUpdateRequest, db: DB) -> UserResponse | None:
    '''
        Update User
    '''
    db_user = await update_user(user, email, db)
    if db_user is None:
        logger.error('User: %s was not found', email)
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'User was not found')

    logger.info('User: %s was updated', email)
    return db_user

@router.delete('/{email}', status_code = status.HTTP_200_OK,
               dependencies = [Depends(BearerToken())])
async def del_user(email: str, db: DB) -> Dict | None:
    '''
        Delete User
    '''
    db_user = await delete_user(email, db)
    if db_user is None:
        logger.error('User: %s can not be deleted, was not found', email)
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = 'User can not be deleted, was not found')

    logger.info('User: %s was deleted', email)
    return {'message': 'User was deleted'}
