from pydantic import BaseModel


class Email(BaseModel):
    email: str

    class Config:
        from_attributes = True


class Login(Email):
    password: str


    class Config:
        from_attributes = True













