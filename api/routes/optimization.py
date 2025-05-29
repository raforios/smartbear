'''
    Optimization: route handlers
'''
import json
from datetime import datetime
from typing import Annotated, List, Dict
from fastapi import APIRouter, Depends, status, Request, HTTPException
from sqlalchemy.orm import Session
from controllers.auth import BearerToken
from controllers.events import create_event
from controllers.optimization import preparing_data, data_ordered, optimization_algorithm
from controllers.optimization import simulation_algorithm, df_to_pydantic
from schemas.events import EventResponse
from schemas.optimization import DataMapResponse, OptimizationResponse, RouteResponse
from services.database import get_db
from services.logger_config import custom_logger as logger

router = APIRouter(prefix = '/api/v1/optimization', tags = ['Optimization'])
DB = Annotated[Session, Depends(get_db)]

@router.get('/data_model', status_code = status.HTTP_200_OK,
            dependencies = [Depends(BearerToken())])
async def get_base_data(request: Request, route_id: int,
            day: int, db: DB) -> List[DataMapResponse] | None:
    '''
        Get data from database befro optimization
    '''
    data = await preparing_data(route_id, day)

    if data is None:
        logger.error('The parameters route_id: %d and day: %d does not have any results',
                    route_id, day)
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
        detail = f'The parameters route_id: {route_id} and day: {day} does not have any results')
    event = EventResponse(
        status = 'success',
        status_code = 200,
        payload = json.dumps({'route_id': route_id, 'day': day, 'process': 'base_data'}),
        response = json.dumps(list(map(lambda d: d.model_dump(), data))),
        event_date = datetime.now(),
        trace_id = ''
    )

    await create_event(request, event, db)
    logger.info('Data: accessed by user')
    return data

@router.get('/distances', status_code = status.HTTP_200_OK,
            dependencies = [Depends(BearerToken())])
async def get_distances(request: Request, route_id: int,
            day: int, db: DB) -> List[OptimizationResponse] | None:
    '''
        Get distances between points
    '''
    dtf_final = await data_ordered(route_id, day)

    if dtf_final is None:
        logger.error('The parameters route_id: %d and day: %d does not have any results',
                    route_id, day)
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
        detail = f'The parameters route_id: {route_id} and day: {day} does not have any results')

    distance = df_to_pydantic(dtf_final, OptimizationResponse)
    event = EventResponse(
        status = 'success',
        status_code = 200,
        payload = json.dumps({'route_id': route_id, 'day': day, 'process': 'base_data'}),
        response = json.dumps(list(map(lambda d: d.model_dump(), distance))),
        event_date = datetime.now(),
        trace_id = ''
    )

    await create_event(request, event, db)
    logger.info('Data: accessed by user')
    return distance

@router.get('/optimal_route', status_code = status.HTTP_200_OK,
            dependencies = [Depends(BearerToken())])
async def get_optimization(request: Request, route_id: int,
            day: int, dist: int, db: DB) -> List[OptimizationResponse] | None:
    '''
        Get optimization data after processing through the optimization algorithm
    '''
    dtf_final = await optimization_algorithm(route_id, day, dist)

    if dtf_final is None:
        logger.error('The parameters route_id: %d and day: %d does not have any results',
                    route_id, day)
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
        detail = f'The parameters route_id: {route_id} and day: {day} does not have any results')
    event = EventResponse(
        status = 'success',
        status_code = 200,
        payload = json.dumps({'route_id': route_id, 'day': day, 'process': 'route_data'}),
        response = json.dumps(list(map(lambda d: d.model_dump(), dtf_final))),
        event_date = datetime.now(),
        trace_id = ''
    )

    await create_event(request, event, db)
    logger.info('Optimization: accessed by user')
    return dtf_final

@router.get('/distance_matrix', status_code = status.HTTP_200_OK,
            dependencies = [Depends(BearerToken())])
async def get_distance_matrix(request: Request, route_id: int, day: int, db: DB) -> Dict | None:
    '''
        Get optimization data after processing through the optimization algorithm
    '''
    dtf_matrix = await simulation_algorithm(route_id, day)

    if dtf_matrix is None:
        logger.error('The parameters route_id: %d and day: %d does not have any results',
                    route_id, day)
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
        detail = f'The parameters route_id: {route_id} and day: {day} does not have any results')
    distance_dict = dtf_matrix.to_dict()
    event = EventResponse(
        status = 'success',
        status_code = 200,
        payload = json.dumps({'route_id': route_id, 'day': day, 'process': 'distance_matrix'}),
        response = dtf_matrix.to_json(double_precision = 4),
        event_date = datetime.now(),
        trace_id = ''
    )

    await create_event(request, event, db)
    logger.info('Distance Matrix: accessed by user')
    return distance_dict

@router.get('/route', status_code = status.HTTP_200_OK,
            dependencies = [Depends(BearerToken())])
async def get_route(request: Request, route_id: int,
            day: int, dist: int, db: DB) -> List[RouteResponse] | None:
    '''
        Get optimization data after processing through the optimization algorithm
    '''
    dtf_route = await optimization_algorithm(route_id, day, dist)

    if dtf_route is None:
        logger.error('The parameters route_id: %d and day: %d does not have any results',
                    route_id, day)
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
        detail = f'The parameters route_id: {route_id} and day: {day} does not have any results')
    event = EventResponse(
        status = 'success',
        status_code = 200,
        payload = json.dumps({'route_id': route_id, 'day': day, 'process': 'route_data'}),
        response = 'json.dumps(list(map(lambda d: d.model_dump(), dtf_route)))',
        event_date = datetime.now(),
        trace_id = ''
    )

    await create_event(request, event, db)
    logger.info('Route: accessed by user')
    return dtf_route
