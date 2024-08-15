from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_session
from app.schemas.auth import UserSchema
from app.schemas.events import EventSchema, EventCreateSchema, AllUserEventsSchema
from app.services.events import create_new_event, get_all_events as get_events, subscribe_event, get_event
from app.services.users import get_current_user

router = APIRouter(prefix="/events", tags=["Events"])


@router.post("", response_model=EventSchema)
def create_event(
        event: EventCreateSchema, session: Session = Depends(get_session)
):
    """
    Создание нового события
    """
    return create_new_event(event, session)


@router.get("", response_model=AllUserEventsSchema)
def get_all_events(
        session: Session = Depends(get_session)
):
    """
    Получение списка всех событий
    """
    return get_events(session)


@router.get("/my", response_model=AllUserEventsSchema)
def get_all_user_events(
        session: Session = Depends(get_session),
        current_user: UserSchema = Depends(get_current_user),
):
    """
    Получить все события, на которые подписан пользователь
    :param session:
    :param current_user:
    :return:
    """
    return get_events(session, current_user)


@router.get("/{event_id}", response_model=EventSchema)
def get_event_by_id(
        event_id: int,
        session: Session = Depends(get_session)
):
    """
    Посмотреть событие по id
    :param event_id:
    :param session:
    :return:
    """
    return get_event(event_id, session)


@router.post("/{event_id}", response_model=UserSchema)
def subscribe_events(
        event_id: int,
        session: Session = Depends(get_session),
        current_user: UserSchema = Depends(get_current_user),
):
    """
    "Подписка" на событие
    """
    return subscribe_event(event_id, current_user, session)


