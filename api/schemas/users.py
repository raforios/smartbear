'''
    User Model
'''
from datetime import datetime
from pydantic import BaseModel, Field

class UserRequest(BaseModel):
    '''
        User Request Class
    '''
    email: str = Field(nullable = False, unique = True, min_length = 5, max_length = 100)
    first_name: str = Field(nullable = False, min_length = 3, max_length = 30)
    last_name: str = Field(nullable = False, min_length = 3, max_length = 30)
    password: str = Field(nullable = False, min_length = 8, max_length = 100)

class UserUpdateRequest(BaseModel):
    '''
        User Update Request Class
    '''
    first_name: str = Field(None, min_length = 3, max_length = 30)
    last_name: str = Field(None, min_length = 3, max_length = 30)
    password: str = Field(None, nmin_length = 8, max_length = 100)
    client: str = Field(None, min_length = 3, max_length = 50)
    status: int = Field(default = 1)

class UserResponse(BaseModel):
    '''
        User Update Request Class
    '''
    email: str
    first_name: str
    last_name: str
    client: str
    role: str
    status: bool
    date_register: datetime
    date_update: datetime
