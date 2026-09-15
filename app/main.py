from fastapi import Depends, FastAPI, HTTPException
from app.database import get_db
from app.models import Author, Book, AuthorCreate

app = FastAPI(title="Bookstore API")


@app.post("/authors")
def create_author(author: AuthorCreate, db=Depends(get_db)):
    new_author = Author(name=author.name)

    db.add(new_author)
    db.commit()
    db.refresh(new_author)

    return new_author

@app.get("/authors")
def get_authors(db=Depends(get_db)):
    authors = db.query(Author).all()
    return authors

@app.get("/authors/{author_id}")
def get_author(author_id: int, db=Depends(get_db)):
    author = db.get(Author, author_id)

    if not author:
        raise HTTPException(status_code=404, detail="Author not found")

    return author

@app.put("/authors/{author_id}")
def update_author(
    author_id: int,
    author: AuthorCreate,
    db=Depends(get_db)
):
    existing_author = db.get(Author, author_id)

    if not existing_author:
        raise HTTPException(status_code=404, detail="Author not found")

    existing_author.name = author.name

    db.commit()
    db.refresh(existing_author)

    return existing_author


@app.delete("/authors/{author_id}")
def delete_author(author_id: int, db=Depends(get_db)):
    author = db.get(Author, author_id)

    if not author:
        raise HTTPException(status_code=404, detail="Author not found")

    db.delete(author)
    db.commit()

    return {"message": "Author deleted successfully"}