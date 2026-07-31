from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.dependency import get_db, get_current_token_payload
from app.schemas.reservation import (
    ReservationRequest,
    ReservationResponse,
)
from app.services.reservation_services import (
    create_reservation,
    cancel_reservation,
)
from app.websockets.broadcast import broadcast_seat_updates


router = APIRouter(prefix="/reservation",tags=["Reservation"])

@router.post("",response_model=ReservationResponse)
async def reserve(
        request:ReservationRequest,
        db:Session=Depends(get_db),
        payload=Depends(get_current_token_payload)
    ):
    result= create_reservation(
        db,
        int(payload["sub"]),
        request
    )
    
    await broadcast_seat_updates(
        result["event_id"],
        result["seat_ids"],
        "reserved",
    )
    return result


@router.delete("/{reservation_id}")
async def cancel(reservation_id: str,payload=Depends(get_current_token_payload)):
    result=cancel_reservation(
        reservation_id,
        int(payload["sub"]),
    )
    await broadcast_seat_updates(
        result["event_id"],
        result["seat_ids"],
        "available",
    )
    return result
    