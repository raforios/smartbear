'''
    Optimization Model
'''
from pydantic import BaseModel

class OptimizationResponse(BaseModel): # pylint: disable=too-few-public-methods
    '''
        Optimization Response Class
    '''
    origin: int
    target: int
    distance: float
    y: float
    x: float

class DataMapResponse(BaseModel): # pylint: disable=too-few-public-methods
    '''
        Simulation Response Class
    '''
    day: int
    client_id: int
    y: float
    x: float
    color: str

class RouteResponse(BaseModel): # pylint: disable=too-few-public-methods
    '''
        Route Response Class
    '''
    # visit_order: int
    origin: int
    target: int
    y: float
    x: float
    y_next: float
    x_next: float
    distance: float
    time_seg: float
    origin_node: int
    destination_node: int
    route: list[int]
