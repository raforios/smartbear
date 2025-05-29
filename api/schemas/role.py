'''
    Role Schema
'''
from enum import Enum

class Role(str, Enum):
    '''
        Role Class with ENUM settings
    '''
    ADMIN = 'ADMIN'
    USER = 'USER'
