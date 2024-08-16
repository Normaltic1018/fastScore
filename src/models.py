from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy import event

from database import Base

class Score(Base):
    __tablename__ = "scores"

    id = Column(Integer, primary_key=True)
    comment = Column(Text, nullable=False)
    amount = Column(Integer, nullable=False)
    date = Column(DateTime, nullable=False)
    team_id = Column(Integer, ForeignKey("teams.id"))

    team = relationship("Team", back_populates="scores")

class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    members = Column(JSON, nullable=False)
    recent_score = Column(Integer, nullable=True)

    scores = relationship('Score', back_populates="team")

@event.listens_for(Score, 'after_insert')
def update_recent_score(mapper, connection, target):
    # 현재 팀의 최근 점수를 가져오고, 새로운 값을 더한 후 업데이트
    team_table = Team.__table__

     # 현재 recent_score 값을 가져오고 새 점수를 더함
    connection.execute(
        team_table.update().
        where(team_table.c.id == target.team_id).
        values(recent_score=(team_table.c.recent_score + target.amount))
    )

class Admin(Base):
    __tablename__ = "admin"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)