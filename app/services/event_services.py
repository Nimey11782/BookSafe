from sqlalchemy.orm import Session

from app.models.event import Event
from app.schemas.event import EventCreate
from app.schemas.seat import SeatStatusResponse
from app.models.seats import Seat
from fastapi import HTTPException
from app.core.redis import redis_client

def create_event(db: Session,event: EventCreate):
    new_event=Event(
        title=event.title,
        description=event.description,
        venue=event.venue,
        start_time=event.start_time,
        total_seats=event.total_seats
    )

    db.add(new_event)
    db.flush()

    combined_seats = []

    for i in range(1, event.total_seats + 1):
        new_seat = Seat(
            event_id=new_event.id,
            seat_number=i,
        )

        combined_seats.append(new_seat)

    db.add_all(combined_seats)#adding all the seats of an event together rather than adding one by one

    db.commit()
    db.refresh(new_event)

    return new_event

#for viewing ALL events
from sqlalchemy import select

def get_all_events(db: Session):
    events = db.scalars(
        select(Event)
    ).all()

    return events

#for returning seats of a particular event
def get_event_seats(db: Session,event_id:int):
    seats=db.scalars(
        select(Seat).where(Seat.event_id==event_id)
    ).all()
    return seats

