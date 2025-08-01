from sqlalchemy.orm import Session
from app.models.user import User
from app.models.news import News
from app.schemas.user import UserCreate
from app.schemas.news import NewsCreate, NewsUpdate
from app.core.security import get_password_hash, verify_password
from typing import Optional

def get_user_by_username(db: Session, username: str) -> Optional[User]:
    return db.query(User).filter(User.username == username).first()

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user: UserCreate) -> User:
    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        password_hash=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
    user = get_user_by_username(db, username)
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user

def get_news_list(db: Session, skip: int = 0, limit: int = 100):
    return db.query(News).offset(skip).limit(limit).all()

def get_news_by_id(db: Session, news_id: int) -> Optional[News]:
    return db.query(News).filter(News.id == news_id).first()

def create_news(db: Session, news: NewsCreate, creator: str) -> News:
    db_news = News(**news.dict(), creator=creator)
    db.add(db_news)
    db.commit()
    db.refresh(db_news)
    return db_news

def update_news(db: Session, news_id: int, news_update: NewsUpdate) -> Optional[News]:
    db_news = db.query(News).filter(News.id == news_id).first()
    if db_news:
        update_data = news_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_news, field, value)
        db.commit()
        db.refresh(db_news)
    return db_news

def delete_news(db: Session, news_id: int) -> bool:
    db_news = db.query(News).filter(News.id == news_id).first()
    if db_news:
        db.delete(db_news)
        db.commit()
        return True
    return False