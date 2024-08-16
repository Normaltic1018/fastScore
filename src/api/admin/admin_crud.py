from models import Admin
from sqlalchemy.orm import Session
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def check_initAdmin(db: Session):
    admin = db.query(Admin).filter_by(username="admin").first()

    if not admin:
        print("Admin is not exist. Create Admin Account...")
        initAdmin = Admin(username="admin", password=pwd_context.hash("1234"))
        
        db.add(initAdmin)
        db.commit()
        db.close()
    else:
        print("Admin is Already exsit")

def get_admin(db: Session, admin: Admin):
    admin = db.query(Admin).get(admin)
    return admin