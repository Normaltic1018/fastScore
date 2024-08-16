from pydantic import BaseModel, field_validator

class Admin(BaseModel):
    username: str

class Token(BaseModel):
    access_token: str
    token_type: str
    username: str