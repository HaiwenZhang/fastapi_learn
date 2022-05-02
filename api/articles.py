from fastapi import APIRouter, Depends, status, HTTPException
from api.db import Article, database
from api.schemas import ArticleSchemaIn, ArticleSchemaOut, UserSchemaIn
from api.toten import get_current_user

router = APIRouter(
    tags = ["Articles"]
)

@router.get("/articles", response_model = list[ArticleSchemaOut])
async def get_articles(current_user: UserSchemaIn = Depends(get_current_user)):
    query = Article.select()
    return await database.fetch_all(query)

@router.post("/articles", 
    status_code = status.HTTP_201_CREATED, 
    response_model = ArticleSchemaOut
)
async def create_article(article:ArticleSchemaIn):
    query = Article.insert().values(
        title = article.title,
        description = article.description
    )
    last_record_id = await database.execute(query)
    return {**article.dict(), "id": last_record_id}

@router.get("/articles/{id}", response_model = ArticleSchemaOut)
async def get_article(id:int):
    query = Article.select().where(id == Article.c.id)
    article = await database.fetch_one(query)

    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article not found!"
        )

    return {**article}

@router.put("/articles/{id", response_model = ArticleSchemaOut)
async def update_article(id:int, article:ArticleSchemaIn):
    query = Article.update().where(Article.c.id == id).values(
        title = article.title,
        description = article.description
    )
    await database.execute(query)
    return {**article.dict(), "id": id}

@router.delete("/articles/{id}")
async def delete_article(id:int):
    query = Article.delete().where(Article.c.id == id)
    await database.execute(query)
    return {"message": "Article deleted"}