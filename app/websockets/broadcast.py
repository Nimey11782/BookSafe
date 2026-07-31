from app.websockets.manager import manager


async def broadcast_seat_updates(
    event_id: int,
    seat_ids: list[int],
    status: str,
):
    updates = [
        {
            "seat_id": seat_id,
            "status": status,
        }
        for seat_id in seat_ids
    ]

    await manager.broadcast_to_event(
        event_id,
        {
            "type": "seat_status_changed",
            "event_id": event_id,
            "updates": updates,
        },
    )