import datetime

from sqlalchemy import cast, func, String
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


def get_book(db: Session, work_id: str):
    return db.query(models.Book).filter(models.Book.work_id == work_id).one()


def get_list(db: Session, skip: int = 0, limit: int = 100):
    return (
        db.query(models.Read)
        .options(joinedload(models.Read.book).options(joinedload(models.Book.authors)))
        .order_by(models.Read.date)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_unmatched_list(db: Session, skip: int = 0, limit: int = 100):
    return (
        db.query(models.UnmatchedRead)
        .order_by(models.UnmatchedRead.date)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_unmatched_list_by_year(db: Session, year: int):
    yearFunc = func.substr(models.UnmatchedRead.date, 1, 4)
    return (
        db.query(models.UnmatchedRead)
        .filter(yearFunc == func.cast(year, String))
        .order_by(models.UnmatchedRead.date)
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


def create_unmatched_read(db: Session, read: schemas.UnmatchedReadCreate):
    db_read = models.UnmatchedRead(**read.dict())
    db.add(db_read)
    db.commit()
    db.refresh(db_read)
    return db_read


# Bleh, this is a mess
def get_read_years(db: Session):
    year = func.substr(models.Read.date, 1, 4)
    reads = (
        db.query(year.label("year"), func.count(year).label("num"))
        .group_by(year)
        .order_by(year)
        .all()
    )

    read_map = {read[0]: read[1] for read in reads}

    year = func.substr(models.UnmatchedRead.date, 1, 4)
    unmatched = (
        db.query(year.label("year"), func.count(year).label("num"))
        .group_by(year)
        .order_by(year)
        .all()
    )

    for read in unmatched:
        if read[0] in read_map.keys():
            read_map[read[0]] += read[1]
        else:
            read_map[read[0]] = read[1]

    return [{"year": year, "num": read_map[year]} for year in sorted(read_map.keys())]


def get_read_year(db: Session, year):
    yearFunc = func.substr(models.Read.date, 1, 4)
    return (
        db.query(models.Read)
        .filter(yearFunc == func.cast(year, String))
        .options(joinedload(models.Read.book).options(joinedload(models.Book.authors)))
        .order_by(models.Read.date)
        .all()
    )


def edit_read(db: Session, read: models.Read, new_date: datetime.date):
    read.date = new_date
    db.commit()
    db.refresh(read)
    return read
