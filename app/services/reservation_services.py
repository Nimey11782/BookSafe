import uuid
import json

from fastapi import HTTPException
from sqlalchemy import select

from app.core.redis import redis_client
from app.schemas.reservation import ReservationRequest
from app.models.seats import Seat
        
def create_reservation(db, user_id: int, request: ReservationRequest):

    reservation_id = str(uuid.uuid4())#uniquely creating for every reservation

    seats=db.scalars(
        select(Seat).where(Seat.id.in_(request.seat_ids))
    ).all()#gets all seats that users want in one query

    #if any seat is missing we must return those particular seats are booked
    validate_seats(seats,request)

    #store the reserved seats in redis : seat->reservation-id 
    reserve_seats_in_redis(seats,reservation_id,)

    store_reservation(reservation_id,user_id,request.seat_ids)

    return {
        "reservation_id": reservation_id,
        "expires_in": 600,
    }

def validate_seats(seats,request):
    requested_ids = set(request.seat_ids)

    found_ids = {
        seat.id
        for seat in seats
    }

    missing_ids = requested_ids - found_ids

    if missing_ids:
        raise HTTPException(
            status_code=404,
            detail=f"Seat(s) {sorted(missing_ids)} do not exist.",
        )

    for seat in seats:
        if seat.is_booked:
            raise HTTPException(
                status_code=400,
                detail=f"Seat {seat.id} is already booked.",
            )
        
def reserve_seats_in_redis(seats,reservation_id: str):
    reserved_seats = []

    for seat in seats:
        success = redis_client.set(
            f"seat:{seat.id}",
            reservation_id,
            nx=True, #using nx so as to create in redis if it does not exist before
            ex=600,
        )
        if success:
            #recording the keys which have been reserved successfully
            reserved_seats.append(seat.id)

        else:
            #rollback the keys if failure occurs
            for reserved_seat in reserved_seats:
                redis_client.delete(
                    f"seat:{reserved_seat}"
                )

            raise HTTPException(
                status_code=400,
                detail=f"Seat {seat.id} is already reserved.",
            )

import json


def store_reservation(
    reservation_id: str,
    user_id: int,
    seat_ids: list[int],
):
    reservation = {
        "user_id": user_id,
        "seat_ids": seat_ids,
    }

    redis_client.set(
        f"reservation:{reservation_id}",
        json.dumps(reservation),
        ex=600,
    )



import json

from fastapi import HTTPException

from app.core.redis import redis_client


def cancel_reservation(reservation_id: str,current_user_id: int):
    
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

    if reservation["user_id"] != current_user_id:
        raise HTTPException(
            status_code=403,
            detail="This reservation does not belong to you.",
        )

    seat_ids = reservation["seat_ids"]

    redis_client.delete(
        f"reservation:{reservation_id}"
    )

    for seat_id in seat_ids:
        redis_client.delete(
            f"seat:{seat_id}"
        )

    return {
        "message": "Reservation cancelled successfully."
    }