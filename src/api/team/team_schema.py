from pydantic import BaseModel, field_validator
from typing import List

# Team Column Info
# id = Column(Integer, primary_key=True)
# name = Column(String, nullable=False)
# members = Column(JSON, nullable=False)
# recent_score = Column(Integer, nullable=True)

class Team(BaseModel):
    id: int
    name: str
    members: List[str] = []
    recent_score: int | None = 0

class TeamCreate(BaseModel):
    name: str
    members: List[str] = []
    recent_score: int = 0

    @field_validator('name')
    def check_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('빈 값은 입력할 수 없습니다.')
        return v
    
class TeamDelete(BaseModel):
    team_id: int

class TeamUpdate(TeamCreate):
    team_id: int