from datetime import datetime
from decimal import Decimal
from enum import unique
from typing import List

from sqlalchemy import String, ForeignKey, text, Boolean, Date, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import expression

from tgbot.models.base import Base, AccountingInteger, TimestampMixin


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    is_bot: Mapped[bool] = mapped_column(Boolean, server_default=expression.false())
    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=True)
    username: Mapped[str] = mapped_column(nullable=True)
    language_code: Mapped[str] = mapped_column(nullable=True, server_default=text("ru_RU"))
    is_premium: Mapped[bool] = mapped_column(Boolean, server_default=expression.false())




