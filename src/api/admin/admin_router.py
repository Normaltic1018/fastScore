from datetime import timedelta, datetime

from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from database import get_db
from api.admin.admin_schema import Token
from api.admin import admin_crud

from api.admin.admin_schema import AdminResetPassword

from models import Admin

router = APIRouter(
    prefix="/api/admin",
)

@router.post("/login", response_model=Token, tags=["Admin"])
def login_for_accessToken(form_data: OAuth2PasswordRequestForm = Depends(),
                          db: Session = Depends(get_db)):
    
    # Check Admin Info
    if not admin_crud.authenticate_admin(db, form_data.username, form_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate" : "Bearer"},
        )

    # Create Token
    data = {
        "sub" : form_data.username,
    }
    access_token = admin_crud.create_aceess_token(data)
    return  Token(access_token=access_token, token_type="bearer", username=form_data.username)

@router.put("/updatePassword", status_code=status.HTTP_202_ACCEPTED, tags=["Admin"])
def password_reset(*, db: Session = Depends(get_db),
                   current_admin: Admin = Depends(admin_crud.get_current_admin),
                   _update_admin: AdminResetPassword):
    admin_crud.change_password(db, current_admin.username, _update_admin.password)

# @router.delete("/resetScore", status_code=status.HTTP_204_NO_CONTENT, tags=["Score"])
# def score_reset(db: Session = Depends(get_db),
#                 current_admin: Admin = Depends(get_current_admin)):
#     score_crud.reset_score(db)