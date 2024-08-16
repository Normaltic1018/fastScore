from datetime import datetime

from sqlalchemy.orm import Session

from api.score.score_schema import ScoreCreate, Score
from models import Score, Team

def get_score_list(db: Session):
    score_list = db.query(Score).order_by(Score.id).all()
    return score_list

def get_score(db: Session, score_id: int):
    score = db.query(Score).get(score_id)
    return score

def create_score(db: Session, team: Team, score_create:ScoreCreate):
    db_score = Score(team=team, comment=score_create.comment, amount=score_create.amount, date=datetime.now())
    db.add(db_score)
    db.commit()

def delete_scroe(db: Session, db_score: Score):
    db.delete(db_score)
    db.commit()

def reset_score(db: Session):
    db.query(Score).delete()
    db.query(Team).update({"recent_score": 0})
    db.commit()