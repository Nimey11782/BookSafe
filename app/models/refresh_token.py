from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base

class RefreshToken(Base):
    __tablename__="refresh_tokens"

    id:Mapped[int]=mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),#to link every token to user also remember one user can have many tokens (phone,laptop)
        nullable=False,
    )

    token_hash: Mapped[str] = mapped_column(
        String,
        nullable=False,
        unique=True,
    )

    expires_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
    )

    revoked: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )