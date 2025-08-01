from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.schemas.news import News, NewsCreate, NewsUpdate
from app.core.crud import get_news_list, get_news_by_id, create_news, update_news, delete_news
from app.core.deps import get_current_user
from app.models.user import User

router = APIRouter()

@router.get("/", response_model=List[News])
def read_news(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    news = get_news_list(db, skip=skip, limit=limit)
    return news

@router.get("/{news_id}", response_model=News)
def read_news_item(news_id: int, db: Session = Depends(get_db)):
    db_news = get_news_by_id(db, news_id=news_id)
    if db_news is None:
        raise HTTPException(status_code=404, detail="News not found")
    return db_news

@router.post("/", response_model=News)
def create_news_item(
    news: NewsCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return create_news(db=db, news=news, creator=current_user.username)

@router.put("/{news_id}", response_model=News)
def update_news_item(
    news_id: int,
    news_update: NewsUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_news = get_news_by_id(db, news_id=news_id)
    if db_news is None:
        raise HTTPException(status_code=404, detail="News not found")
    
    if db_news.creator != current_user.username:
        raise HTTPException(status_code=403, detail="Not authorized to update this news")
    
    updated_news = update_news(db=db, news_id=news_id, news_update=news_update)
    return updated_news

@router.delete("/{news_id}")
def delete_news_item(
    news_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_news = get_news_by_id(db, news_id=news_id)
    if db_news is None:
        raise HTTPException(status_code=404, detail="News not found")
    
    if db_news.creator != current_user.username:
        raise HTTPException(status_code=403, detail="Not authorized to delete this news")
    
    success = delete_news(db=db, news_id=news_id)
    if success:
        return {"message": "News deleted successfully"}
    else:
        raise HTTPException(status_code=500, detail="Failed to delete news")