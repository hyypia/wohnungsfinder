from datetime import datetime
from typing import TypeAlias
from dataclasses import dataclass


Id: TypeAlias = str


@dataclass(slots=True, frozen=True)
class User:
    user_id: Id
    date: datetime
    wbs: str
    square: float
    rooms: float


def wrire_user() -> None:
    pass


def get_user() -> User:
    return User
