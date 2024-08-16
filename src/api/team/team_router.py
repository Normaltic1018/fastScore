from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session

from database import get_db
from api.team import team_schema, team_crud

router = APIRouter(
    prefix="/api/team",
)

@router.get("/list", response_model=List[team_schema.Team], status_code=status.HTTP_200_OK, tags=["Team"])
def team_list(db: Session = Depends(get_db)):
    _team_list = team_crud.get_team_list(db)
    return _team_list

@router.get("/detail/{team_id}", response_model=team_schema.Team, status_code=status.HTTP_200_OK, tags=["Team"])
def team_detail(team_id: int, db: Session = Depends(get_db)):
    team = team_crud.get_team(db, team_id)
    return team

@router.post("/create", response_model=team_schema.TeamCreate, status_code=status.HTTP_201_CREATED, tags=["Team"])
def team_create(_team_create: team_schema.TeamCreate, db: Session = Depends(get_db)):
    team_crud.create_team(db, team_create=_team_create)
    return _team_create

@router.delete("/delete", response_model=team_schema.TeamDelete, status_code=status.HTTP_202_ACCEPTED, tags=["Team"])
def team_delete(_team_delete: team_schema.TeamDelete,
                db: Session = Depends(get_db)):
    db_team = team_crud.get_team(db, team_id=_team_delete.team_id)
    if not db_team:
        raise HTTPException(status_code=400,
                            detail="등록되지 않은 팀입니다.")
    team_crud.delete_question(db, db_team=db_team)
    return _team_delete

@router.put("/update", response_model=team_schema.TeamUpdate, status_code=status.HTTP_202_ACCEPTED, tags=["Team"])
def team_update(_team_update: team_schema.TeamUpdate,
                db: Session = Depends(get_db)):
    db_team = team_crud.get_team(db, team_id=_team_update.team_id)
    if not db_team:
        raise HTTPException(status_code=400,
                            detail="등록되지 않은 팀입니다.")
    team_crud.update_team(db, db_team=db_team, team_update=_team_update)
    return _team_update