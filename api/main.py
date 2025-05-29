'''
Machine Learning API
'''
import socket
from datetime import datetime
from datetime import date
from typing import Dict

import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

# HTTPException, status
# from fastapi.security import OAuth2PasswordRequestForm
# from services.security import create_token

from dotenv import dotenv_values
from routes.auth import router as auth_router
from routes.events import router as events_router
from routes.optimization import router as optimization_router
from routes.geo_points import router as geo_points_router
from routes.users import router as users_router
from services.database import Base, engine

PARAMETERS = dotenv_values('.env')


app = FastAPI(
    title = 'Business Intelligence Service',
    description = 'Machine Learning API for Business Intelligence',
    version = '1.0.0'
)

# Moutn static files
app.mount('/static', StaticFiles(directory = 'static'), name = 'static')

# Root path (Healtcheck function)
@app.get('/api/v1', tags = ['Home'])
def root() -> Dict | None:
    '''
    Function root
    '''
    today = datetime.now()
    copyright_symbol = '\u00A9'
    output = {
        'Api Healthcheck': 'OK',
        'Host': socket.gethostname(),
        'Environment': 'prod',
        'Status': 'available',
        'Server Date Time': today,
        'Last Update': date.today(),
        'Application': 'Python - FastAPI',
        'Database': 'PostgreSQL Database',
        'Owner': f'BearSoft {copyright_symbol} {today.year}'
    }
    return output


# Include routers
app.include_router(auth_router, tags = ['Authentication'])
app.include_router(events_router, tags = ['Events'])
app.include_router(optimization_router, tags = ['Optimization'])
app.include_router(geo_points_router, tags = ['GeoPoints'])
app.include_router(users_router, tags = ['Users'])

# @app.post('/login', tags = ['Authentication'])
# async def login(form_data: OAuth2PasswordRequestForm = Depends()):
#     '''
#         Login endpoint
#     '''
#     user = authenticate_user(form_data.email, form_data.password)
#     if not user:
#         raise HTTPException(
#             status_code = status.HTTP_401_UNAUTHORIZED,
#             detail = 'Incorrect email or password',
#             headers = {'WWW-Authenticate': 'Bearer'},
#         )
#     data = {'email': form_data.email, 'password': form_data.password}
#     token = create_token(data)
#     print(f'TOKEN: {token}')

#     return Token(access_token = token, token_type = 'bearer')


# Entry point to run the app
if __name__ == '__main__':
    Base.metadata.create_all(bind = engine)
    uvicorn.run('main:app', host = PARAMETERS.get('HOST'),
            port = int(PARAMETERS.get('PORT')), reload = True)
