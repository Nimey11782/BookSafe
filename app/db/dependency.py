from collections.abc import Generator

from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from fastapi import HTTPException

def get_db() -> Generator[Session,None,None]:
    db=SessionLocal()
    try:
        yield db #yield closes automatically therefore better to use yield than return
    finally:
        db.close()


from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.security import verify_token

security = HTTPBearer()
#HTTPBearer() reads the HTTP request.
# Authorization: Bearer eyJhbGc...
# It extracts
# Bearer & eyJhbGc...

def get_current_token_payload(credentials: HTTPAuthorizationCredentials = Depends(security)):
    #bearer becomes credentials.scheme 
    #token becomes credentials.credentials 

    token = credentials.credentials

    payload = verify_token(token)

    if payload["type"] != "access":
        raise HTTPException(
            status_code=401,
            detail="Invalid token type",
        )

    return payload