from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.dependency import get_db
from app.schemas.auth import UserCreate, UserLogin, UserResponse, Token
from app.services.auth_services import create_user, login_user

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/signup",response_model=UserResponse)
def signup(user:UserCreate,db:Session=Depends(get_db)):
    return create_user(db,user)


@router.post("/login",response_model=Token)
def login(user: UserLogin, db: Session = Depends(get_db)):
    return login_user(db, user)


from app.db.dependency import get_current_token_payload

@router.post("/me")
def me(payload=Depends(get_current_token_payload)):
    return payload


#writing this for refreshing the refresh token
from app.schemas.auth import RefreshRequest
from app.services.auth_services import refresh_access_token

@router.post("/refresh", response_model=Token)
def refresh(request: RefreshRequest,db: Session = Depends(get_db)):
    return refresh_access_token(
        db,
        request.refresh_token,
    )

from app.services.auth_services import logout_user
@router.post("/logout")
def logout(
    request: RefreshRequest,
    db: Session = Depends(get_db),
):
    return logout_user(
        db,
        request.refresh_token,
    )