# BookSafe

BookSafe is a concurrent ticket booking backend built with FastAPI, PostgreSQL, Redis, and WebSockets. The project focuses on handling multiple users trying to reserve or book the same seat at the same time while keeping seat availability synchronized across connected clients.

The system uses temporary Redis-backed reservations with expiration, transactional booking confirmation, and row-level database locking to prevent double booking under concurrent requests. WebSockets are used to broadcast reservation, booking, and cancellation events so that every connected client sees seat availability updates in real time.

## Features

- JWT-based authentication and authorization
- Event and seat management
- Temporary seat reservations using Redis
- Transactional booking confirmation
- Real-time seat updates using WebSockets
- Concurrency-safe booking using `SELECT ... FOR UPDATE`
- REST APIs documented with Swagger

## Tech Stack

- FastAPI
- PostgreSQL
- Redis
- SQLAlchemy
- WebSockets
- JWT Authentication
- Alembic

## Running the project

```bash
git clone https://github.com/Nimey11782/BookSafe.git
cd BookSafe

python -m venv .venv
pip install -r requirements.txt

docker start redis

uvicorn app.main:app --reload
```

Swagger UI is available at:

```
http://127.0.0.1:8000/docs
```

## Future Improvements

- Docker Compose
- Payment gateway integration
- Automatic WebSocket updates on reservation expiry
- Deployment
