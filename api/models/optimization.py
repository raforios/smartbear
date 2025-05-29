'''
    Optimization Model
'''
from sqlalchemy import String, Integer, Float, Column
from services.database import Base

class Optimization(Base): # pylint: disable=too-few-public-methods
    '''
        Optimization Class
    '''
    __tablename__ = 'routes'
    id = Column(Integer, primary_key = True)
    route_id = Column(Integer)
    day = Column(Integer)
    client_id = Column(Integer)
    client = Column(String(255))
    latitude = Column(Float)
    longitude = Column(Float)
