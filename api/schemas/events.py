'''
    Events Model
'''
from datetime import datetime
from pydantic import BaseModel

class EventResponse(BaseModel): # pylint: disable=too-few-public-methods
    '''
        Register Response Class
    '''
    status: str
    status_code: int
    payload: str
    response: str
    event_date: datetime
    trace_id: str
