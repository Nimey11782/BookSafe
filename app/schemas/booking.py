from pydantic import BaseModel
from datetime import datetime

class ConfirmBookingRequest(BaseModel):
    reservation_id: str

