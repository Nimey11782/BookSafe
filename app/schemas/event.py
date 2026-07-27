from pydantic import BaseModel
from datetime import datetime

class EventCreate(BaseModel):
    title: str
    description: str
    venue: str
    start_time: datetime
    total_seats: int


class EventResponse(BaseModel):
    id: int
    title: str
    description: str
    venue: str
    start_time: datetime
    total_seats: int

    model_config = {
        "from_attributes": True
    }