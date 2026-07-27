from pydantic import BaseModel
from datetime import datetime

class BookingRequest(BaseModel):
    seat_id: int

class BookingResponse(BaseModel):
    seat_id: int
    booked_at: datetime

    model_config = {
        "from_attributes": True
    }