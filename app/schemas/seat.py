from pydantic import BaseModel


class SeatResponse(BaseModel):
    seat_number: int
    is_booked: bool

    model_config = {
        "from_attributes": True
    }