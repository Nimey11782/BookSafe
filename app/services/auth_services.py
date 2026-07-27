from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.user import User #db user will have these 
from app.schemas.auth import UserCreate #response from user about name and pass
from app.core.security import hash_password


def create_user(db:Session, user:UserCreate) -> User:
    #checking same name must not exist before
    existing_user = db.scalar(#scaler returns atmost one row i.e. in sql query a limit of 1 is set
        select(User).where(User.username == user.username)#new approach is using select instead of query
    )

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )

    new_user=User(#creating new user obj using SQLAlchemy to be inserted in db 
        username=user.username,
        password_hash=hash_password(user.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)#fetching latest row from db

    return new_user


# now doing login
from app.schemas.auth import UserLogin
from app.core.security import (
    verify_password,
    create_access_token,
    create_refresh_token
)
from datetime import datetime, timedelta, timezone

from app.models.refresh_token import RefreshToken
from app.core.config import REFRESH_TOKEN_EXPIRE_DAYS

def login_user(db: Session, user: UserLogin):
    #finding the row with same username 
    db_user = db.scalar(
        select(User).where(User.username == user.username)
    )

    if not db_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"#donot print username not exist that would help attackers
        )

    if not verify_password(
        user.password,
        db_user.password_hash
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    # since now password is verified, generate jwt token
    access_token = create_access_token(
        {
            "sub": str(db_user.id),
            "type": "access",
        }
    )
    refresh_token = create_refresh_token(
        {
            "sub": str(db_user.id),
            "type": "refresh",
        }
    )
    #save the refresh token after hashing in db
    hashed_refresh_token = hash_password(refresh_token)

    db_refresh_token = RefreshToken(
        user_id=db_user.id,
        token_hash=hashed_refresh_token,
        expires_at=datetime.now(timezone.utc)
            + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS),
    )

    db.add(db_refresh_token)
    db.commit()

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

#refresh the refresh token
from app.core.security import verify_token
def refresh_access_token(db:Session,refresh_token:str):
    #first verify the refresh token
    payload=verify_token(refresh_token)

    if payload["type"] != "refresh":
        raise HTTPException(
            status_code=401,
            detail="Invalid token type",
        )

    user_id = int(payload["sub"])

    matched_refresh_token=validate_refresh_token(
        db,
        user_id,
        refresh_token
    )

    matched_refresh_token.revoked=True #revoke the old token i.e. invalidating it

    db.add(matched_refresh_token)
    #generate new refresh token
    new_refresh_token = create_refresh_token(
        {
            "sub": str(user_id),
            "type": "refresh",
        }
    )
    # Store new refresh token
    db_refresh_token = RefreshToken(
        user_id=user_id,
        token_hash=hash_password(new_refresh_token),
        expires_at=datetime.now()
        + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS),
    )

    db.add(db_refresh_token)
    db.commit()

    #since the access token was expired ,now create a new and return 
    access_token = create_access_token(
        {
            "sub": str(user_id),
            "type": "access",
        }
    )
    return {
        "access_token": access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer",
    }
#for refreshing refresh token we need to match it from user whether that user is still valid and not revoked then only we will allow to generate new access token without login  again
def validate_refresh_token(
    db: Session,
    user_id: int,
    refresh_token: str,
):
    db_refresh_tokens = db.scalars(
        select(RefreshToken).where(
            RefreshToken.user_id == user_id
        )
    ).all()

    matched_token = None

    for token in db_refresh_tokens:
        if verify_password(
            refresh_token,
            token.token_hash,
        ):
            matched_token = token
            break

    if matched_token is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid refresh token",
        )

    if matched_token.revoked:
        raise HTTPException(
            status_code=401,
            detail="Refresh token revoked",
        )

    if matched_token.expires_at < datetime.now():
        raise HTTPException(
            status_code=401,
            detail="Refresh token expired",
        )
    return matched_token
    
#for logout , same logic flow with that of validate refresh token since first we will validate it and then make the refresh token as invalid
def logout_user(
    db: Session,
    refresh_token: str,
):
    payload = verify_token(refresh_token)

    if payload["type"] != "refresh":
        raise HTTPException(
            status_code=401,
            detail="Invalid token type",
        )

    user_id = int(payload["sub"])

    matched_refresh_token = validate_refresh_token(
        db,
        user_id,
        refresh_token,
    )

    matched_refresh_token.revoked = True

    db.commit()

    return {
        "message": "Logged out successfully"
    }