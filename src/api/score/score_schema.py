import datetime
from pydantic import BaseModel, field_validator

    # Score
    # id = Column(Integer, primary_key=True)
    # comment = Column(Text, nullable=False)
    # amount = Column(Integer, nullable=False)
    # date = Column(DateTime, nullable=False)
    # team_id = Column(Integer, ForeignKey("teams.id"))

class ScoreCreate(BaseModel):
    comment: str
    amount : int = 0

    @field_validator('comment')
    def check_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('빈 값은 입력할 수 없습니다.')
        return v
    
class Score(BaseModel):
    id: int
    comment: str
    amount: int
    date: datetime.datetime

class ScoreDelete(BaseModel):
    id: int