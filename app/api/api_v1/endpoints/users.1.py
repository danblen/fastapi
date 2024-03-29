from typing import Annotated, Any, List

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic.networks import EmailStr
from sqlmodel import select

from app import crud
from app.api.deps import (
    CurrentUser,
    SessionDep,
    get_current_active_superuser,
)
from app.core.config import settings
from app.models import User, UserCreate, UserCreateOpen, UserOut, UserUpdate
from app.utils import send_new_account_email

router = APIRouter()


@router.get("/", dependencies=[Depends(get_current_active_superuser)])
def read_users(session: SessionDep, skip: int = 0, limit: int = 100) -> List[UserOut]:
    """
    Retrieve users.
    """
    statement = select(User).offset(skip).limit(limit)
    users = session.exec(statement).all()
    return users  # type: ignore


@router.post("/", dependencies=[Depends(get_current_active_superuser)])
def create_user(*, session: SessionDep, user_in: UserCreate) -> UserOut:
    """
    Create new user.
    """
    user = crud.get_user_by_email(session=session, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )

    user = crud.create_user(session=session, user_create=user_in)
    if settings.EMAILS_ENABLED and user_in.email:
        send_new_account_email(
            email_to=user_in.email, username=user_in.email, password=user_in.password
        )
    return user  # type: ignore


@router.get("/me")
def read_user_me(session: SessionDep, current_user: CurrentUser) -> UserOut:
    """
    Get current user.
    """
    return current_user  # type: ignore


@router.post("/open")
def create_user_open(session: SessionDep, user_in: UserCreateOpen) -> UserOut:
    """
    Create new user without the need to be logged in.
    """
    if not settings.USERS_OPEN_REGISTRATION:
        raise HTTPException(
            status_code=403,
            detail="Open user registration is forbidden on this server",
        )
    user = crud.get_user_by_email(session=session, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system",
        )
    user_create = UserCreate.from_orm(user_in)
    user = crud.create_user(session=session, user_create=user_create)
    return user  # type: ignore


@router.get("/{user_id}")
def read_user_by_id(
    user_id: int, session: SessionDep, current_user: CurrentUser
) -> UserOut:
    """
    Get a specific user by id.
    """
    user = session.get(User, user_id)
    if user == current_user:
        return user  # type: ignore
    if not current_user.is_superuser:
        raise HTTPException(
            # TODO: Review status code
            status_code=400,
            detail="The user doesn't have enough privileges",
        )
    return user  # type: ignore
