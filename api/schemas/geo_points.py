'''
    Points Model
'''
from pydantic import BaseModel, Field

class GeoPointRequest(BaseModel):
    '''
        Geo Point Create Request Class
    '''
    client_id: int = Field(nullable = False, gt = 0)
    client: str = Field(nullable = False, min_length = 3, max_length = 255)
    latitude: float = Field(nullable = False)
    longitude: float = Field(nullable = False)

class ListGeoPointsRequest(BaseModel):
    '''
        List Geo Points Request Class
    '''
    route_id: int = Field(nullable = False, gt = 0)
    day: int = Field(nullable = False, gt = 0)
    locations: list[GeoPointRequest]

class ListDataRequest(BaseModel):
    '''
        List Data Request Class
    '''
    data: list[ListGeoPointsRequest]

class GeoPointUpdateRequest(BaseModel):
    '''
        Geo Point Update Request Class
    '''
    route_id: int = Field(None, gt = 0)
    day: int = Field(None, gt = 0)
    client_id: int = Field(None, gt = 0)
    client: str = Field(nullable = True, min_length = 3, max_length = 255)
    latitude: float = Field(None)
    longitude: float = Field(None)

class GeoPointResponse(BaseModel):
    '''
        Geo Point Response Class
    '''
    route_id: int
    day: int
    client_id: int
    client: str
    latitude: float
    longitude: float
