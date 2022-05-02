from pydantic import BaseModel

class ArticleSchema(BaseModel):
    title: str
    description: str


class MyArticleSchema(ArticleSchema):
    id: int
    title: str
    description: str