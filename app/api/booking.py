from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.dependency import get_db, get_current_token_payload
from app.schemas.booking import ConfirmBookingRequest
from app.services.booking_services import confirm_booking

router=APIRouter(prefix="/booking",tags=["Bookings"])

@router.post("/confirm")
def book(
    request:ConfirmBookingRequest,
    payload=Depends(get_current_token_payload),
    db:Session=Depends(get_db)
):
    return confirm_booking(
        db,
        request.reservation_id,
        int(payload["sub"]),
    )