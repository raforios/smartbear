'''
    Optimization: route handlers
'''
from typing import Annotated, Dict
from fastapi import APIRouter, Depends, status, Request, HTTPException
from sqlalchemy.orm import Session
from controllers.auth import BearerToken
from controllers.geo_points import create_geo_points, update_geo_point, delete_geo_point
from schemas.geo_points import ListDataRequest, GeoPointUpdateRequest, GeoPointResponse
from services.database import get_db
from services.logger_config import custom_logger as logger

router = APIRouter(prefix = '/api/v1/geo_points', tags = ['GeoPoints'])
DB = Annotated[Session, Depends(get_db)]

@router.post('/', status_code = status.HTTP_201_CREATED,
            dependencies = [Depends(BearerToken())])
async def post_geo_points(request: Request, data: ListDataRequest, db: DB) -> Dict | None:
    '''
        Loading data through endpoint called from client side
    '''
    db_data = await create_geo_points(request, data, db)
    if db_data is None:
        logger.error('The database is not available or has a problem')
        raise HTTPException(status_code = status.HTTP_503_SERVICE_UNAVAILABLE,
                            detail = 'The database is not available or has a problem')


    logger.info('Geo Points: All data was loaded successfully on API database')
    return {'message': 'All data was loaded successfully'}

@router.patch('/', status_code = status.HTTP_200_OK,
            dependencies = [Depends(BearerToken())])
async def patch_geo_point (route_id: int, client_id: int, day: int,
            point: GeoPointUpdateRequest, db: DB) -> GeoPointResponse | None:
    '''
        Update Geo Point
    '''
    db_route = await update_geo_point(point, route_id, client_id, day, db)
    if db_route is None:
        logger.error('Geo Point: %d was not found', route_id)
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'Route was not found')

    logger.info('Geo Point: %d was updated', route_id)
    return db_route

@router.delete('/', status_code = status.HTTP_200_OK,
               dependencies = [Depends(BearerToken())])
async def del_geo_point(route_id: int, client_id: int, day: int, db: DB) -> Dict | None:
    '''
        Delete Geo Point
    '''
    db_user = await delete_geo_point(route_id, client_id, day, db)
    if db_user is None:
        logger.error('Geo Point: %d can not be deleted, was not found', route_id)
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = 'Geo point can not be deleted, was not found')

    logger.info('Geo Point: %d was deleted', route_id)
    return {'message': 'The user was deleted'}
