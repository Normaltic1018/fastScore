import os,sys
# 현재 모듈의 상위 디렉토리 경로
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from database import SessionLocal
from models import Team, Score

t = Team(name="segfault", members=["normaltic","doldol"])

db = SessionLocal()
db.add(t)
db.commit()
