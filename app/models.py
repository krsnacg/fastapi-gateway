from pydantic import BaseModel

class ConfigRoute():
    def __init__(self, id: str, uri: str, predicate: str, auth_required: bool = False):
        self.id = id
        self.uri = uri
        self.predicate = predicate
        self.auth_required = auth_required

class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    username: str | None = None

class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None
        
class UserInDB(User):
    hashed_password: str
    