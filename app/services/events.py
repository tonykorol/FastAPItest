from datetime import datetime, UTC

from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from app.models import Event, User
from app.schemas.auth import UserSchema
from app.schemas.events import EventCreateSchema, AllUserEventsSchema, EventSchema


def create_new_event(event: EventCreateSchema, session: Session) -> Event:
    event_model = Event(**event.model_dump())
    session.add(event_model)
    session.commit()
    session.refresh(event_model)
    return event_model


def get_all_events(session: Session, current_user: UserSchema = None) -> AllUserEventsSchema:
    if current_user:
        events = session.query(Event).filter(Event.users)
    else:
        events = session.query(Event).filter(Event.meeting_time >= datetime.now(UTC))
    return {"events": events}


def subscribe_event(event_id: int, current_user: UserSchema, session: Session) -> UserSchema:
    event = session.query(Event).filter(Event.id == event_id).first()
    if event is None:
        raise HTTPException(status_code=404, detail="Invalid event id")
    event.users = [current_user]
    session.commit()
    return current_user


def get_event(event_id: int, session: Session) -> EventSchema:
    event = session.query(Event).filter(Event.id == event_id).first()
    if event is None:
        raise HTTPException(status_code=404, detail="Invalid event id")
    return event
