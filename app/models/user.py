from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base

#creating a table User -> in more technical terms -> this python class represents a table user
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False
    )
    password_hash:Mapped[str]=mapped_column(
        String,
        nullable=False
    )
