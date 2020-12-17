import datetime

from sqlalchemy.orm import joinedload, Session

from . import models, schemas


def get_author(db: Session, author_id: str):
    return db.query(models.Author).filter(models.Author.ol_id == author_id).first()


def get_book(db: Session, work_id: str):
    return db.query(models.Book).filter(models.Book.work_id == work_id).first()


def get_read(db: Session, date: datetime.date, book: str):
    return (
        db.query(models.Read)
        .filter(models.Read.ol_book_id == book, models.Read.date == date)
        .first()
    )


def create_author(db: Session, author: schemas.AuthorCreate):
    db_author = models.Author(**author.dict())
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def get_authors(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Author).offset(skip).limit(limit).all()


def get_books(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Book).offset(skip).limit(limit).all()


def get_list(db: Session, skip: int = 0, limit: int = 100):
    return (
        db.query(models.Read)
        .options(joinedload(models.Read.book).options(joinedload(models.Book.authors)))
        .order_by(models.Read.date)
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_book(db: Session, book: schemas.BookCreate):
    authors = (
        db.query(models.Author)
        .filter(models.Author.ol_id.in_(book.author_ol_ids))
        .all()
    )
    db_book = models.Book(
        work_id=book.work_id,
        edition_id=book.edition_id,
        image_id=book.image_id,
        title=book.title,
        authors=authors,
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def create_read(db: Session, read: schemas.ReadCreate):
    db_read = models.Read(**read.dict())
    db.add(db_read)
    db.commit()
    db.refresh(db_read)
    return db_read
