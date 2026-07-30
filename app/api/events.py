from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.dependency import get_db
from app.schemas.event import EventCreate, EventResponse 
from app.schemas.seat import SeatResponse
from app.services.event_services import create_event,get_all_events,get_event_seats

from app.services.seat_services import get_event_seats
from app.schemas.seat import SeatStatusResponse 

router = APIRouter(prefix="/events",tags=["Events"])

@router.post("",response_model=EventResponse)
def create(event:EventCreate,db:Session=Depends(get_db)):
    return create_event(
        db,
        event,
    )

#get all current events listed
@router.get("",response_model=list[EventResponse])
def get_events(db:Session=Depends(get_db)):
    return get_all_events(db)

#get all current seats of an event

@router.get("/{event_id}/seats",response_model=list[SeatResponse])
def get_seats(event_id:int,db:Session=Depends(get_db)):
    return get_event_seats(db,event_id)

@router.get("/{event_id}/seats/",response_model=list[SeatStatusResponse])
def get_seat_statuses(event_id:int,db:Session=Depends(get_db)):
    return get_event_seats(db,event_id)#not applying auth since anyone should be able to see the status of seats of event
