'''
    Events Controller
'''
from typing import List
from fastapi import Request
from models.events import Event
from schemas.events import EventResponse
from controllers.users import get_current_user

async def create_event(request: Request, event: EventResponse, db) -> Event | None:
    '''
        Create event
    '''
    bearer = request.headers.get('Authorization')
    token = bearer.replace('Bearer ', '')
    user = await get_current_user(token, db)
    event.trace_id = user.email
    event = Event(**event.model_dump())
    db.add(event)
    db.commit()
    db.refresh(event)
    return event

async def read_events(db) -> List[EventResponse] | None:
    '''
        Read All Events from Database
    '''
    events = db.query(Event).all()
    if not events:
        return []
    return events

async def read_event(event_id: int, db) -> EventResponse | None:
    '''
        Read Event by id from Database
    '''
    event = db.query(Event).filter(Event.id == event_id).first()
    if event is None:
        return None
    return event
