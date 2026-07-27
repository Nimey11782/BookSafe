from pydantic import BaseModel, Field

class UserCreate(BaseModel):
    username: str=Field(min_length=3, max_length=50)
    password: str = Field(min_length=6)

class UserResponse(BaseModel):
    id:int

class UserLogin(BaseModel):#usercreate would have worked but we are adding it for future if suppose signup requires something additional
    username: str
    password: str

class Token(BaseModel):
    access_token:str
    refresh_token: str
    token_type:str

class RefreshRequest(BaseModel):
    refresh_token: str
