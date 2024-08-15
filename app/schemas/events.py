from datetime import datetime

from pydantic import BaseModel, Field


class EventBaseSchema(BaseModel):
    name: str = Field(..., max_length=100)
    meeting_time: datetime
    description: str = Field(..., max_length=300)


class EventSchema(EventBaseSchema):
    id: int


class EventCreateSchema(EventBaseSchema):
    pass


class AllUserEventsSchema(BaseModel):
    events: list[EventSchema]
