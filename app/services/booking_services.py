from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.booking import Booking
from app.models.seats import Seat

def book_seat(db:Session,user_id:int,seat_id:int):
    #the frontend would send seat_id and not seat_number bcoz then it would also have to send the event_id
    seat=db.scalar(
        select(Seat).where(Seat.id==seat_id)
    )
    if seat is None:
        raise HTTPException(
            status_code=404,
            detail="Seat not found",
        )

    if seat.is_booked:
        raise HTTPException(
            status_code=400,
            detail="Seat already booked",
        )

    seat.is_booked = True

    booking = Booking(
        user_id=user_id,
        seat_id=seat_id
    )

    db.add(booking)
    db.commit()
    return {
        "message": "Seat booked successfully"
    }

#to check user own bookings
def get_my_bookings(db: Session,user_id: int):
    return db.scalar(
        select(Booking).where(Booking.user_id==user_id)
    ).all()
