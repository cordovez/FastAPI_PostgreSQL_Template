from pydantic import BaseModel


class UserSchema(BaseModel):
    username: str
    email: str
    is_admin: bool = False
