from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.booking import Booking
from app.models.seats import Seat
import time

import json
from app.core.redis import redis_client

def confirm_booking(db:Session,reservation_id: str,current_user_id: int,):

    reservation = redis_client.get(
        f"reservation:{reservation_id}"
    )
    if reservation is None:
        raise HTTPException(
            status_code=400,
            detail="Reservation expired or not found.",
        )
    reservation = json.loads(
        reservation
    )

    if reservation["user_id"] != current_user_id: #very imp coz if someone steal the uuid one can steal your reservation
        raise HTTPException(
            status_code=403,
            detail="This reservation does not belong to you.",
        )

    seat_ids = reservation["seat_ids"]

    #the frontend would send seat_id and not seat_number bcoz then it would also have to send the event_id
    seats = db.scalars(
        select(Seat).where(Seat.id.in_(seat_ids)).with_for_update()
    ).all()

    if len(seats) != len(seat_ids):
        raise HTTPException(
            status_code=404,
            detail="One or more seats do not exist.",
        )
    for seat in seats:
        if seat.is_booked:
            raise HTTPException(
                status_code=400,
                detail=f"Seat {seat.id} is already booked.",
            )

    for seat in seats:
        seat.is_booked = True
        booking = Booking(
            user_id=current_user_id,
            seat_id=seat.id,
        )
        db.add(booking) #add each seat in db only after all checks

    db.commit()
    
    #since booking is done , reservation is no longer needed
    redis_client.delete(
        f"reservation:{reservation_id}"
    )

    for seat in seats:
        redis_client.delete(
            f"seat:{seat.id}"
        )

    

    return {
        "message": "Booking confirmed successfully.",
        "event_id": seats[0].event_id,
        "seats": seat_ids,
    }

#to check user own bookings
def get_my_bookings(db: Session,user_id: int):
    return db.scalars(
        select(Booking).where(Booking.user_id==user_id)
    ).all()
