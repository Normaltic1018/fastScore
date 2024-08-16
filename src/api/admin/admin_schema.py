from pydantic import BaseModel, field_validator

class Admin(BaseModel):
    username: str