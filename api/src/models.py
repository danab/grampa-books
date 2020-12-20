from sqlalchemy import (
    Boolean,
    Column,
    Date,
    DateTime,
    func,
    ForeignKey,
    Integer,
    String,
    Table,
)
from sqlalchemy.orm import relationship

from .database import Base

association_table = Table(
    "books_to_authors",
    Base.metadata,
    Column("book_id", Integer, ForeignKey("books.work_id")),
    Column("author_id", Integer, ForeignKey("authors.ol_id")),
)


class Book(Base):
    __tablename__ = "books"

    work_id = Column(String, primary_key=True, index=True)
    edition_id = Column(String, index=True)
    title = Column(String, unique=True, index=True)
    image_id = Column(String)
    created = Column(DateTime, server_default=func.now())

    authors = relationship("Author", secondary=association_table)
    reads = relationship("Read", back_populates="book")


class Author(Base):
    __tablename__ = "authors"

    ol_id = Column(String, primary_key=True, index=True)
    name = Column(String)
    created = Column(DateTime, server_default=func.now())

    books = relationship("Book", secondary=association_table)


class Read(Base):
    __tablename__ = "reads"

    date = Column(Date, primary_key=True, index=True)
    ol_book_id = Column(
        String, ForeignKey("books.work_id"), primary_key=True, index=True
    )
    submitter_comment = Column(String)
    initials = Column(String)
    created = Column(DateTime, server_default=func.now())

    book = relationship("Book", back_populates="reads")


class UnmatchedRead(Base):
    __tablename__ = "unmatched_reads"

    read_key = Column(Integer, primary_key=True)
    date = Column(Date, index=True)
    title = Column(String, index=True)
    author = Column(String, index=True)
    submitter_comment = Column(String)
    initials = Column(String)
    created = Column(DateTime, server_default=func.now())
