'''
    User Model
'''
from datetime import datetime
from sqlalchemy import String, Integer, DateTime, Column, Boolean, Enum
from services.database import Base
from schemas.role import Role

class User(Base): # pylint: disable=too-few-public-methods
    '''
        Users Class
    '''
    __tablename__ = 'users'
    id = Column(Integer, primary_key = True, index = True)
    email = Column(String(100), unique = True)
    first_name = Column(String(30))
    last_name = Column(String(30))
    client = Column(String(30))
    password = Column(String(100), nullable = False)
    role = Column(Enum(Role), default = Role.USER)
    status = Column(Boolean, default = True)
    date_register = Column(DateTime, default = datetime.now())
    date_update = Column(DateTime, default = datetime.now())
