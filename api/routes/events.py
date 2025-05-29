'''
    Events: route handlers
'''
from typing import Annotated, List
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from controllers.auth import BearerToken
from controllers.events import read_events, read_event
from schemas.events import EventResponse
from services.database import get_db
from services.logger_config import custom_logger as logger

router = APIRouter(prefix = '/api/v1/events', tags = ['Events'])
DB = Annotated[Session, Depends(get_db)]

@router.get('/', status_code = status.HTTP_200_OK,
            dependencies = [Depends(BearerToken())])
async def get_events(db: DB) -> List[EventResponse] | None:
    '''
        List events
    '''
    events = await read_events(db)
    logger.info('Events: accessed by user')
    return events

@router.get('/{event_id}', status_code = status.HTTP_200_OK,
            dependencies = [Depends(BearerToken())])
async def get_event(event_id: int, db: DB) -> EventResponse | None:
    '''
        List event by id
    '''
    event = await read_event(event_id, db)
    if event is None:
        logger.error('Event: %d was not found', event_id)
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'Event was not found')

    logger.info('Event: %d was found', event_id)
    return event
