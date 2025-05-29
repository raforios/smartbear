'''
    Events Model
'''
from datetime import datetime
from sqlalchemy import String, Integer, DateTime, Column
from services.database import Base

class Event(Base): # pylint: disable=too-few-public-methods
    '''
        Events Class
    '''
    __tablename__ = 'events'
    id = Column(Integer, primary_key = True, index = True)
    status = Column(String(50), nullable = False)
    status_code = Column(Integer, nullable = False)
    payload = Column(String(length = None))
    response = Column(String(length = None))
    event_date = Column(DateTime, default = datetime.now())
    trace_id = Column(String(50))
