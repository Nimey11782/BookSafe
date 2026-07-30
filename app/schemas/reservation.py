from pydantic import BaseModel

class ReservationRequest(BaseModel):
    seat_ids: list[int]


class ReservationResponse(BaseModel):
    reservation_id: str
    expires_in: int