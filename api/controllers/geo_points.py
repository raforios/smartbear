'''
    Geo Points Controller
'''
import json
from typing import List
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from controllers.events import create_event
from models.optimization import Optimization
from schemas.geo_points import GeoPointUpdateRequest, GeoPointResponse
from schemas.events import EventResponse

async def read_geo_points(db) -> List[Optimization] | None:
    '''
        Read All Geo Points from Database
    '''
    routes = db.query(Optimization).all()
    if not routes:
        return []
    return routes

async def read_geo_point(route_id: int,
            client_id: int, day: int, db) -> Optimization | None:
    '''
        Read Geo Point by client_id, route_id, day from Database
    '''
    point = db.query(Optimization).filter(Optimization.route_id == route_id,
            Optimization.client_id == client_id, Optimization.day == day).first()

    if point is None:
        return None
    return point

async def create_geo_points(request, data, db) -> List[Optimization] | None:
    '''
        Creating Geo points into the database
    '''
    try:
        db_data = []
        counter = 0
        for item in data.data:
            route_id = item.route_id
            day = item.day
            exist = db.query(Optimization).filter(Optimization.route_id == route_id,
                            Optimization.day == day).first()
            if exist:
                db.query(Optimization).filter(Optimization.route_id == route_id,
                            Optimization.day == day).delete(synchronize_session = False)
                db.commit()
            last_id = db.query(Optimization).order_by(Optimization.id.desc()).first()
            if last_id:
                counter = last_id.id
            for location in item.locations:
                counter += 1
                register = Optimization(id = counter,
                            route_id = route_id, day = day,
                            client_id =  location.client_id,
                            client = location.client, longitude = location.longitude,
                            latitude = location.latitude)
                db_data.append(register)

        db.add_all(db_data)
        db.commit()
        event = EventResponse(
            status = 'success',
            status_code = 201,
            payload = json.dumps(data.model_dump()),
            response = json.dumps({'message': 'All data was loaded successfully'}),
            event_date = datetime.now(),
            trace_id = ''

        )
        await create_event(request, event, db)

        return db_data
    except SQLAlchemyError as error:
        return error

async def update_geo_point(point: GeoPointUpdateRequest, route_id: int,
            client_id: int, day: int, db) -> GeoPointResponse | None:
    '''
        Update Geo Point
    '''
    db_point = db.query(Optimization).filter(Optimization.route_id == route_id,
            Optimization.client_id == client_id, Optimization.day == day).first()
    if db_point is None:
        return None

    if point.route_id is not None and point.route_id > 0 and isinstance(point.route_id, int):
        db_point.route_id = point.route_id
    if point.day is not None and point.day > 0 and isinstance(point.day, int):
        db_point.day = point.day
    if point.client is not None and isinstance(point.client, str):
        db_point.client = point.client
    if  isinstance(point.latitude, float) and point.latitude != 0:
        db_point.latitude = point.latitude
    if  isinstance(point.longitude, float) and point.latitude != 0:
        db_point.longitude = point.longitude
    db.commit()
    db.refresh(db_point)
    point_response = GeoPointResponse(
        route_id = db_point.route_id,
        day = db_point.day,
        client_id = db_point.client_id,
        client = db_point.client,
        longitude = db_point.longitude,
        latitude = db_point.latitude
    )

    return point_response

async def delete_geo_point(route_id: int,
            client_id: int, day: int, db) -> Optimization | None:
    '''
        Delete Geo Point
    '''
    db_point = db.query(Optimization).filter(Optimization.route_id == route_id,
            Optimization.client_id == client_id, Optimization.day == day).first()

    if db_point:
        db.delete(db_point)
        db.commit()
        return db_point

    return None
