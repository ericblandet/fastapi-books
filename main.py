import os

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware, db

from models import Author, Book
from schema import Author as SchemaAuthor
from schema import Book as SchemaBook

app = FastAPI()
load_dotenv(".env")

app.add_middleware(DBSessionMiddleware, db_url=os.environ['DB_URL'])


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/add-author/", response_model=SchemaAuthor)
def add_author(author: SchemaAuthor):
    db_author = Author(
        name=author.name,
        age=author.age,
    )
    db.session.add(db_author)
    db.session.commit()
    return db_author


@app.post("/add-book/", response_model=SchemaBook)
def add_book(book: SchemaBook):
    db_book = Book(title=book.title,
                   rating=book.rating,
                   author_id=book.author_id)
    db.session.add(db_book)
    db.session.commit()
    return db_book


@app.get("/books/")
def get_books():
    books = db.session.query(Book).all()
    return books


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)