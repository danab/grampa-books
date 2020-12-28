import datetime
from typing import List

from pydantic import BaseModel


class AuthorBase(BaseModel):
    ol_id: str
    name: str


class AuthorCreate(AuthorBase):
    pass


class Author(AuthorBase):
    class Config:
        orm_mode = True


class BookBase(BaseModel):
    work_id: str
    edition_id: str = None
    image_id: str = None
    title: str


class BookCreate(BookBase):
    author_ol_ids: List[str]


class Book(BookBase):
    class Config:
        orm_mode = True


class BookWithAuthor(Book):
    authors: List[Author]


class AuthorWithBooks(Author):
    books: List[Book]


class ReadBase(BaseModel):
    date: datetime.date
    ol_book_id: str
    submitter_comment: str = None
    initials: str


class ReadCreate(ReadBase):
    pass


class Read(ReadBase):
    class Config:
        orm_mode = True


class ReadWithBook(Read):
    book: BookWithAuthor


class YearCount(BaseModel):
    year: int
    num: int

    class Config:
        orm_mode = True


class LeaderCount(BaseModel):
    initials: str
    num: int

    class Config:
        orm_mode = True


class UnmatchedReadBase(BaseModel):
    date: datetime.date
    title: str
    author: str = None
    submitter_comment: str
    initials: str


class UnmatchedReadCreate(UnmatchedReadBase):
    pass


class UnmatchedRead(UnmatchedReadBase):
    read_key: int

    class Config:
        orm_mode = True


class YearReads(BaseModel):
    reads: List[ReadWithBook]
    unmatched: List[UnmatchedRead]


class BookWithReads(BookWithAuthor):
    reads: List[Read]


class AuthorWithReads(Author):
    books: List[BookWithReads]

    class Config:
        orm_mode = True
