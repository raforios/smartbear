'''
    Auth Schema
'''
from pydantic import BaseModel, Field, EmailStr

class LoginRequest(BaseModel):
    '''
        LoginRequest Class
    '''
    email: EmailStr = Field(min_length = 5, max_length = 50,
                    description = 'User email for login.')
    password: str = Field(min_length = 8, max_length = 100,
                    description = 'User password for login.')

class SignupResponse(BaseModel):
    '''
        SignupResponse Class
    '''
    user_email: EmailStr = Field(...,
                    description = 'Email of the newly registered user.')
    message: str = Field(...,
                    description = 'Confirmation message for successful signup.')

class Token(BaseModel):
    '''
        Token Class
    '''
    access_token: str = Field(...,
                    description = 'JWT access token for authentication.')
    token_type: str = Field(...,
                    description = 'Type of the token, typically "bearer".')
