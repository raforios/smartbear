'''
    Auth Schema
'''
from pydantic import BaseModel, Field

class LoginRequest(BaseModel):
    '''
        LoginRequest Class
    '''
    email: str = Field(nullable = False, unique = True, min_length = 5, max_length = 50)
    password: str = Field(nullable = False, min_length = 8, max_length = 100)

class SignupResponse(BaseModel):
    '''
        SignupResponse Class
    '''
    user_email: str
    message: str

class Token(BaseModel):
    '''
        Token Class
    '''
    access_token: str
    token_type: str
