from pydantic import BaseModel, constr


class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    card_number: constr(min_length=16, max_length=16)
    pin_code: constr(min_length=4, max_length=4)
