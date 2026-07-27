from datetime import datetime

from sqlalchemy import String, DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship

from app.db.database import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.seats import Seat

class Event(Base):
    __tablename__="events"

    id:Mapped[int]= mapped_column(primary_key=True)
    
    title: Mapped[str] = mapped_column(String)

    description: Mapped[str] = mapped_column(String)

    venue: Mapped[str] = mapped_column(String)

    start_time: Mapped[datetime] = mapped_column(DateTime)

    total_seats: Mapped[int] = mapped_column(Integer)

    seats: Mapped[list["Seat"]] = relationship(
        back_populates="event",
    )