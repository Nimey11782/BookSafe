from datetime import datetime

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base

class Booking(Base):
    __tablename__="bookings"

    id:Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )

    seat_id: Mapped[int] = mapped_column(
        ForeignKey("seats.id"),
        nullable=False,
    )

    booked_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
    )