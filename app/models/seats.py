from sqlalchemy import Boolean, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base

class Seat(Base):
    __tablename__ = "seats"

    id: Mapped[int] = mapped_column(primary_key=True)

    event_id: Mapped[int] = mapped_column(
        ForeignKey("events.id"),
        nullable=False,
    )

    seat_number: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    is_booked: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    event = relationship(
        "Event",
        back_populates="seats",
    )