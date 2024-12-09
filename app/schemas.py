from pydantic import BaseModel


class UserID(BaseModel):
    user_id: int

    class Config:
        from_attributes = True


class Token(UserID):
    token: str
    

    class Config:
        from_attributes = True













