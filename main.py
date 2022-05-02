from fastapi import FastAPI, HTTPException, status
from fastapi.params import Depends
from sqlalchemy.orm import Session
from api.database import engine, sessionLocal
from api import models
from api.schemas import ArticleSchema, MyArticleSchema

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/articles/", response_model=MyArticleSchema)
def add_article(article:ArticleSchema, db:Session=Depends(get_db)):
    new_article = models.Article(
        title=article.title, 
        description=article.description
    )
    db.add(new_article)
    db.commit()
    db.refresh(new_article)
    return new_article


@app.get("/articles/", response_model=list[MyArticleSchema])
def get_articles(db:Session=Depends(get_db)):
    articles = db.query(models.Article).all()
    return articles


@app.get("/articles/{id}", status_code=status.HTTP_200_OK)
def get_article(id:int, db:Session=Depends(get_db)):
    article = db.query(models.Article).filter(
        models.Article.id == id
    ).first()

    if article:
        return article
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        message="Article was not found!")

@app.put("/articles/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=MyArticleSchema)
def update_article(id:int, article: ArticleSchema ,db:Session=Depends(get_db)):
    db.query(models.Article).filter(
        models.Article.id == id
    ).update({
        "title": article.title, 
        "description": article.description
    })
    article = db.query(models.Article).filter(models.Article.id == id).first()
    return article

@app.delete("/articles/{id}", status_code=status.HTTP_202_ACCEPTED)
def delete_article(id:int,db:Session=Depends(get_db)):
    db.query(models.Article).filter(
        models.Article.id == id
    ).delete(synchronize_session=False)
    db.commit()

    return {"msg": "success"}

