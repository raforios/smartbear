
'''
    Auth Controller
'''
from fastapi import Request
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials

class BearerToken(HTTPBearer): # pylint: disable=too-few-public-methods
    '''
        BearerToken Class
    '''
    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        return await super().__call__(request)
