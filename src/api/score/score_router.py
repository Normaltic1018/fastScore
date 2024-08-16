from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from api.score import score_schema, score_crud
from api.team import team_crud

from typing import List

from api.admin.admin_crud import get_current_admin
from models import Admin

router = APIRouter(
    prefix="/api/score",
)

@router.get("/list", response_model=List[score_schema.Score], 
            status_code=status.HTTP_200_OK, tags=["Score"])
def score_list(db: Session = Depends(get_db)):
    _score_list = score_crud.get_score_list(db)
    return _score_list

@router.post("/addScore/{team_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Score"])
def score_create(team_id: int, _score_create: score_schema.ScoreCreate,
                 db: Session = Depends(get_db),
                 current_admin: Admin = Depends(get_current_admin)):
    team = team_crud.get_team(db, team_id=team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not Found")
    score_crud.create_score(db, team=team,
                            score_create=_score_create)

@router.delete("/delete" , status_code=status.HTTP_202_ACCEPTED, 
               response_model=score_schema.Score, tags=["Score"])
def score_delete(_score_delete: score_schema.ScoreDelete,
                 db: Session = Depends(get_db),
                 current_admin: Admin = Depends(get_current_admin)):
    db_score = score_crud.get_score(db, score_id=_score_delete.id)

    if not db_score:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="없는 점수입니다.")
    score_crud.delete_scroe(db, db_score=db_score)
    return _score_delete

@router.delete("/resetScore", status_code=status.HTTP_204_NO_CONTENT, tags=["Score"])
def score_reset(db: Session = Depends(get_db),
                current_admin: Admin = Depends(get_current_admin)):
    score_crud.reset_score(db)