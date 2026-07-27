from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.dependency import get_db, get_current_token_payload
from app.schemas.booking import BookingRequest
from app.services.booking_services import book_seat

router=APIRouter(prefix="/booking",tags=["Bookings"])

@router.post("")
def book(
    request:BookingRequest,
    payload=Depends(get_current_token_payload),
    db:Session=Depends(get_db)
):
    return book_seat(
        db,
        int(payload["sub"]),
        request.seat_id
    )