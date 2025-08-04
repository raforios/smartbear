'''
    Localization Schemas
'''
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

class LocalizationBaseSchema(BaseModel):
    '''
        Base schema with `from_attributes=True` enabled to handle
        ORM objects like those from SQLAlchemy.
    '''
    model_config = ConfigDict(from_attributes=True)

class PointBase(BaseModel):
    '''
        Base schema for a geographical point.
    '''
    latitude: float = Field(
        ..., ge = -90.0, le = 90.0,
        description = 'The latitude of the geographical point.'
    )
    longitude: float = Field(
        ..., ge = -180.0, le = 180.0,
        description = 'The longitude of the geographical point.'
    )

class PlannedPointSchema(PointBase, LocalizationBaseSchema):
    '''
        Schema for a point in a planned route.
    '''
    point_name: str = Field(
        ..., max_length=100,
        description = 'Name of the planned point, e.g., "Office A".'
    )
    reference_data: Optional[str] = Field(
        None, max_length = 255,
        description = 'Additional reference data or notes for the point.'
    )

class PlannedRouteCreateSchema(BaseModel):
    '''
        Schema for creating a planned route.
    '''
    route_name: str = Field(
        ..., max_length = 150,
        description = 'Name of the planned route.'
    )
    description: Optional[str] = Field(
        None, max_length = 500,
        description = 'Description of the route.'
    )
    user_id: int = Field(
        ...,
        description = 'ID of the user creating the route.'
    )
    points: List[PlannedPointSchema] = Field(
        ...,
        description = 'A list of geographical points for the route.'
    )

class PlannedRouteResponseSchema(PlannedRouteCreateSchema, LocalizationBaseSchema):
    '''
        Response schema for a planned route, including the database ID.
    '''
    id: int
    created_at: datetime

class ExecutedRouteCreateSchema(BaseModel):
    '''
        Schema for creating a new executed route instance.
    '''
    user_id: int = Field(
        ...,
        description = 'ID of the user for this executed route.'
    )
    planned_route_id: Optional[int] = Field(
        None,
        description = 'ID of the planned route to which this executed route corresponds.'
    )

class ExecutedRouteResponseSchema(ExecutedRouteCreateSchema, LocalizationBaseSchema):
    '''
        Response schema for a created executed route, including the database ID.
    '''
    id: int
    start_time: datetime
    end_time: Optional[datetime]

class ExecutedPointCreateSchema(PointBase):
    '''
        Schema for a point in an executed route, sent from a mobile device.
    '''
    executed_route_id: int = Field(
        ...,
        description = 'ID of the executed route this point belongs to.'
    )
    timestamp: datetime = Field(
        ...,
        description = 'Timestamp when the point was registered.'
    )

class ExecutedPointResponseSchema(ExecutedPointCreateSchema, LocalizationBaseSchema):
    '''
        Response schema for an executed point, including the database ID.
    '''
    id: int

class AttendanceCreateSchema(BaseModel):
    '''
        Schema for creating an attendance record.
    '''
    user_id: int = Field(
        ...,
        description = 'ID of the user making the check-in/check-out.'
    )
    planned_point_id: int = Field(
        ...,
        description = 'ID of the planned point where attendance is being logged.'
    )
    check_in_time: Optional[datetime] = Field(
        None,
        description = 'Timestamp for the check-in time.'
    )
    check_out_time: Optional[datetime] = Field(
        None,
        description = 'Timestamp for the check-out time.'
    )

class AttendanceResponseSchema(AttendanceCreateSchema, LocalizationBaseSchema):
    '''
        Response schema for an attendance record, including the database ID.
    '''
    id: int

class PointsVisitedResponseSchema(BaseModel):
    '''
        Response schema for the points visited statistics endpoint.
    '''
    user_id: int
    total_points_visited: int
    points_details: List[dict] # Use dict for flexible point details

class RouteComparisonSchema(LocalizationBaseSchema):
    '''
        Schema for a single route comparison result.
    '''
    planned_route_id: int
    planned_route_name: str
    executed_route_id: Optional[int]
    match_percentage: float = Field(
        ..., ge = 0.0, le = 100.0,
        description='Percentage of the executed route that matches the planned one.'
    )
    points_visited_count: int

class RouteComparisonsResponseSchema(LocalizationBaseSchema):
    '''
        Response schema for the route comparisons endpoint.
    '''
    comparisons: List[RouteComparisonSchema]
