import datetime
from typing import List

from fastapi import Body, Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from starlette.middleware.cors import CORSMiddleware

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins="http://localhost:8080",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/authors/", response_model=schemas.AuthorWithBooks)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    db_author = crud.get_author(db, author_id=author.ol_id)
    if db_author:
        raise HTTPException(status_code=400, detail="Author already exists")
    return crud.create_author(db=db, author=author)


@app.get("/authors/", response_model=List[schemas.AuthorWithBooks])
def read_authors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    authors = crud.get_authors(db, skip=skip, limit=limit)
    return authors


@app.get("/authors/{author}", response_model=schemas.AuthorWithBooks)
def read_author(author_id: str, db: Session = Depends(get_db)):
    db_author = crud.get_author(db, author_id=author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author


@app.post("/books/", response_model=schemas.BookWithAuthor)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    db_book = crud.get_book(db, work_id=book.work_id)
    if db_book:
        raise HTTPException(status_code=400, detail="book already exists")
    return crud.create_book(db=db, book=book)


@app.get("/books/", response_model=List[schemas.BookWithAuthor])
def read_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    books = crud.get_books(db, skip=skip, limit=limit)
    return books


@app.get("/books/search", response_model=List[schemas.BookWithAuthor])
def search_books(title: str, db: Session = Depends(get_db)):
    books = crud.search_books(db, title)
    return books


@app.get("/books/{work_id}", response_model=schemas.BookWithReads)
def read_book(work_id: str, db: Session = Depends(get_db)):
    book = crud.get_book(db, "/works/" + work_id)
    return book


@app.get("/reads/", response_model=List[schemas.ReadWithBook])
def read_list(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    read_list = crud.get_list(db, skip=skip, limit=limit)
    return read_list


@app.post("/reads/", response_model=schemas.ReadWithBook)
def create_read(read: schemas.ReadCreate, db: Session = Depends(get_db)):
    db_read = crud.get_read(db, date=read.date, book=read.ol_book_id)
    if db_read:
        raise HTTPException(status_code=400, detail="read already exists")
    return crud.create_read(db=db, read=read)


@app.get("/reads/year", response_model=List[schemas.YearCount])
def read_years(db: Session = Depends(get_db)):
    return crud.get_read_years(db)


@app.get("/reads/year/{year}", response_model=schemas.YearReads)
def read_single_year(year: int, db: Session = Depends(get_db)):
    return {
        "reads": crud.get_read_year(db, year),
        "unmatched": crud.get_unmatched_list_by_year(db, year),
    }


@app.get("/unmatched_reads/")  # , response_model=List[schemas.ReadWithBook])
def unmatched_read_list(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    read_list = crud.get_unmatched_list(db, skip=skip, limit=limit)
    return read_list


@app.post("/unmatched_reads/", response_model=schemas.UnmatchedRead)
def create_unmatched_read(
    read: schemas.UnmatchedReadCreate, db: Session = Depends(get_db)
):
    return crud.create_unmatched_read(db=db, read=read)


@app.post("/edit_read_date/", response_model=schemas.ReadWithBook)
def edit_read_date(
    date: datetime.date = Body(...),
    book_id: str = Body(...),
    new_date: datetime.date = Body(...),
    db: Session = Depends(get_db),
):
    db_read = crud.get_read(db, date=date, book="/works/" + book_id)
    if not db_read:
        raise HTTPException(status_code=400, detail="can't find read")
    return crud.edit_read(db, db_read, new_date)
