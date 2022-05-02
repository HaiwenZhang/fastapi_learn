from pydantic import BaseModel

class ArticleSchemaIn(BaseModel):
    title:str
    description:str

class ArticleSchemaOut(ArticleSchemaIn):
    id:int


class UserSchemaIn(BaseModel):
    username:str
    password:str

class UserSchemaOut(UserSchemaIn):
    id:int


class LoginSchema(BaseModel):
    username:str
    password:str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None
    scopes: list[str] = []
