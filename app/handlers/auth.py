from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_session
from app.schemas.auth import UserCreateSchema, UserSchema, TokenPairSchema, UserCredentialsSchema, RefreshTokenSchema, \
    AccessTokenSchema, AllUsersSchema
from app.services.auth import create_jwt_token_pair, refresh_access_token
from app.services.users import create_user, get_user_by_credentials, get_current_user, get_all_users_list

router = APIRouter(prefix="/auth", tags=["User authorisation/registration"])


@router.post("/users", response_model=UserSchema)
def register_user(
        user: UserCreateSchema, session: Session = Depends(get_session)
):
    """Регистрация нового пользователя"""
    try:
        return create_user(session, user)
    except IntegrityError:
        raise HTTPException(status_code=422, detail="User already exists")


@router.get("/users", response_model=AllUsersSchema)
def get_all_users(
        current_user: UserSchema = Depends(get_current_user),
        session: Session = Depends(get_session)
):
    return get_all_users_list(current_user, session)


@router.post("/token", response_model=TokenPairSchema)
def get_tokens(user_data: UserCredentialsSchema, session: Session = Depends(get_session)):
    user = get_user_by_credentials(session, user_data.username, user_data.password)
    return create_jwt_token_pair(user_id=user.id)


@router.post("/token/refresh", response_model=AccessTokenSchema)
def refresh_token(token: RefreshTokenSchema):
    return AccessTokenSchema(access_token=refresh_access_token(token.refresh_token))


@router.get("/me", response_model=UserSchema)
def get_current_user(current_user: UserSchema = Depends(get_current_user)):
    return current_user
