from models import Team
from sqlalchemy.orm import Session

from api.team.team_schema import TeamCreate, TeamUpdate

def get_team_list(db: Session):
    team_list = db.query(Team).order_by(Team.id).all()
    return team_list

def get_team(db: Session, team_id: int):
    team = db.query(Team).get(team_id)
    return team

def create_team(db: Session, team_create: TeamCreate):
    db_team = Team(name=team_create.name, members=team_create.members,
                   recent_score=0)
    db.add(db_team)
    db.commit()

def delete_question(db: Session, db_team: Team):
    db.delete(db_team)
    db.commit()

def update_team(db: Session, db_team: Team, team_update: TeamUpdate):
    db_team.name = team_update.name
    db_team.members = team_update.members
    db.add(db_team)
    db.commit()

def reset_team(db: Session):
    db.query(Team).delete()
    db.commit()