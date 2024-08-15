from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound

from fastapi import Depends, HTTPException

from app.database import get_session
from app.models import User
from app.schemas.auth import UserCreateSchema, UserSchema, AllUsersSchema
from app.services.auth import oauth2_scheme, _get_token_payload, USER_IDENTIFIER
from app.services.encrypt import encrypt_password, validate_password


def create_user(session: Session, user: UserCreateSchema) -> User:
    user_model = User(**user.model_dump())

    user_model.password = encrypt_password(user_model.password)

    session.add(user_model)  # Создание пользователя
    session.commit()
    session.refresh(user_model)  # Нужно для получения ID
    return user_model


def get_current_user(
        token: str = Depends(oauth2_scheme),
        session: Session = Depends(get_session, use_cache=True)
) -> User:
    payload = _get_token_payload(token, "access")
    try:
        # user = User.get(session, id=payload[USER_IDENTIFIER])
        query = select(User).where(User.id == payload[USER_IDENTIFIER])
        result = session.execute(query)
        result.unique()
        return result.scalar_one()

    except NoResultFound:
        raise HTTPException(status_code=401, detail="Cloud not validate credentials")
    return user


def get_all_users_list(
    current_user: UserSchema,
    session: Session,
) -> AllUsersSchema:
    if current_user.is_admin:
        query = select(User)
        result = session.execute(query)
        result.unique()
        return {"users": [r[0].username for r in result]}
    else:
        raise HTTPException(status_code=401, detail="Not admin")


def get_user_by_credentials(session: Session, username: str, password: str) -> User:
    try:
        query = select(User).where(User.username == username)
        result = session.execute(query)
        result.unique()
        user = result.scalar_one()

    except NoResultFound:
        raise HTTPException(status_code=401, detail="Cloud not validate credentials")

    if not validate_password(password, user.password):
        raise HTTPException(status_code=401, detail="Cloud not validate credentials")

    return user
