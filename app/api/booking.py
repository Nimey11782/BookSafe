from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.dependency import get_db, get_current_token_payload
from app.schemas.booking import ConfirmBookingRequest
from app.services.booking_services import confirm_booking
from app.websockets.broadcast import broadcast_seat_updates

router=APIRouter(prefix="/booking",tags=["Bookings"])

@router.post("/confirm")
async def book(
    request:ConfirmBookingRequest,
    payload=Depends(get_current_token_payload),
    db:Session=Depends(get_db)
):
    result=confirm_booking(
        db,
        request.reservation_id,
        int(payload["sub"]),
    )
    await broadcast_seat_updates(
        result["event_id"],
        result["seat_ids"],
        "booked",
    )
    return result

