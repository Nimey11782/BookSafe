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

router = APIRouter(prefix="/reservation",tags=["Reservation"])

@router.post("",response_model=ReservationResponse)
def reserve(
        request:ReservationRequest,
        db:Session=Depends(get_db),
        payload=Depends(get_current_token_payload)
    ):
    return create_reservation(
        db,
        int(payload["sub"]),
        request
    )


@router.delete("/{reservation_id}")
def cancel(reservation_id: str,payload=Depends(get_current_token_payload)):
    return cancel_reservation(
        reservation_id,
        int(payload["sub"]),
    )
    