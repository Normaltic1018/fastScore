from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api.team import team_router
from api.score import score_router

from api.admin.admin_crud import check_initAdmin

from database import SessionLocal
from models import Admin

app = FastAPI()

# CORS 등록
# origins = [
#     "http://127.0.0.1",
# ]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

def initProc():
    db = SessionLocal()
    admin = check_initAdmin(db)


initProc() 
app.include_router(team_router.router)
app.include_router(score_router.router)