from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api.team import team_router

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

app.include_router(team_router.router)