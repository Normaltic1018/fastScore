from models import Admin
from sqlalchemy.orm import Session
from passlib.context import CryptContext
import jwt
from jwt.exceptions import InvalidTokenError
from datetime import datetime, timedelta, timezone

from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status

from database import get_db

SECRET_KEY = "ea3a8e7c290473e6ad2bd9565ac9b3c285cc194b0cd670b56170d69e5e749ebd"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/admin/login")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_hashedPassword(password):
    return pwd_context.hash(password)

def check_initAdmin(db: Session):
    admin = db.query(Admin).filter_by(username="admin").first()

    if not admin:
        print("Admin is not exist. Create Admin Account...")
        initAdmin = Admin(username="admin", password=get_hashedPassword("1234"))
        
        db.add(initAdmin)
        db.commit()
        db.close()
    else:
        print("Admin is Already exsit")

def get_admin(db: Session, username: str):
    return db.query(Admin).filter(Admin.username == username).first()

def authenticate_admin(db:Session, username: str, password: str):
    admin = get_admin(db, username)
    if not admin:
        return False
    if not verify_password(password, admin.password):
        return False
    
    return admin

def create_aceess_token(data: dict, expires_delta: timedelta | None = timedelta(minutes=15)):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + expires_delta

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_admin(token: str = Depends(oauth2_scheme),
                db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid Credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        
    except InvalidTokenError:
        raise credentials_exception
    else:
        admin = get_admin(db, username=username)
        if admin is None:
            raise create_aceess_token
        return admin
    
def change_password(db: Session, username: str, password: str):
    admin = db.query(Admin).filter_by(username=username).first()

    admin.password = get_hashedPassword(password)
    db.add(admin)
    db.commit()