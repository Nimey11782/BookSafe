from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.seats import Seat
from app.schemas.seat import SeatStatusResponse
from fastapi import HTTPException
from app.core.redis import redis_client


def get_event_seats(db: Session, event_id: int):
    seats = db.scalars(
        select(Seat).where(
            Seat.event_id == event_id
        )
    ).all()

    if not seats:
        raise HTTPException(
            status_code=404,
            detail=f"No seats found for event with ID {event_id}.",
        )

    response = []

    for seat in seats:
        if seat.is_booked:
            status = "booked"

        elif redis_client.exists(f"seat:{seat.id}"):
            status = "reserved"

        else:
            status = "available"

        response.append(
            SeatStatusResponse(
                id=seat.id,
                seat_number=seat.seat_number,
                status=status,
            )
        )

    return response