from datetime import datetime

from sqlalchemy import String, Table, Column, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

# events_users = Table("events_users", Base.metadata,
#                      Column("user_id", ForeignKey("users.id"), primary_key=True),
#                      Column("events_id", ForeignKey("events.id"), primary_key=True),
#                      )


# _________СДЕЛАТЬ МИГРАЦИИ_______________
# ПОТОМ ТОЛЬКО ПРОДОЛЖАТЬ(ОСТАНОВИЛСЯ НА СОЗДАНИИ ПРОМЕЖУТОЧНОЙ ТАБЛИНЫ
# ПОСМОТРЕТЬ СХЕМЫ И УБРАТЬ ИЗ СХЕМЫ ЭВЕНТОВ ВСЕХ ЮЗЕРОВ (ОНИ ТАМ НЕ НУЖНЫ)
#



class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True)
    email: Mapped[str] = mapped_column(String(254), unique=True)
    password: Mapped[str]
    is_admin: Mapped[bool] = mapped_column(Boolean, nullable=True, default=False)

    events: Mapped[list["Event"]] = relationship(secondary="events_users", back_populates="users")


class Event(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    meeting_time: Mapped[datetime]
    description: Mapped[str] = mapped_column(String(300))

    users: Mapped[list["User"]] = relationship(secondary="events_users", back_populates="events")


class EventsUsers(Base):
    __tablename__ = "events_users"

    event_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("events.id"), primary_key=True)
