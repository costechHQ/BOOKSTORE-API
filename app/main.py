from fastapi import Cookie, Depends, FastAPI, HTTPException, Response
from app.database import get_db
from app.models import Author, Book, AuthorCreate, BookCreate, User, UserCreate
from passlib.context import CryptContext

app = FastAPI(title="Bookstore API")

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def require_session(
    session: str | None = Cookie(default=None)
):
    if not session:
        raise HTTPException(
            status_code=401,
            detail="Authentication required"
        )

    return session



@app.post("/login")
def login_user(
    user: UserCreate,
    response: Response,
    db=Depends(get_db)
):
    existing_user = db.query(User).filter(
        User.username == user.username
    ).first()

    if not existing_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    password_correct = pwd_context.verify(
        user.password,
        existing_user.password
    )

    if not password_correct:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    response.set_cookie(
        key="session",
        value=str(existing_user.id)
    )

    return {
        "message": "Login successful"
    }


@app.post("/logout")
def logout_user(response: Response):
    response.delete_cookie(key="session")

    return {
        "message": "Logout successful"
    }

@app.post("/authors")
def create_author(
    author: AuthorCreate,
    db=Depends(get_db),
    session=Depends(require_session)
):
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
    db=Depends(get_db),
    session=Depends(require_session)
):
    existing_author = db.get(Author, author_id)

    if not existing_author:
        raise HTTPException(status_code=404, detail="Author not found")

    existing_author.name = author.name

    db.commit()
    db.refresh(existing_author)

    return existing_author


@app.delete("/authors/{author_id}")
def delete_author(
    author_id: int,
    db=Depends(get_db),
    session=Depends(require_session)
):
    author = db.get(Author, author_id)

    if not author:
        raise HTTPException(status_code=404, detail="Author not found")

    db.delete(author)
    db.commit()

    return {"message": "Author deleted successfully"}


@app.post("/books")
def create_book(book: BookCreate, db=Depends(get_db)):
    author = db.get(Author, book.author_id)

    if not author:
        raise HTTPException(status_code=404, detail="Author not found")

    new_book = Book(
        title=book.title,
        author_id=book.author_id
    )

    db.add(new_book)
    db.commit()
    db.refresh(new_book)

    return new_book


@app.get("/books")
def get_books(db=Depends(get_db)):
    books = db.query(Book).all()
    return books


@app.get("/books/{book_id}")
def get_book(book_id: int, db=Depends(get_db)):
    book = db.get(Book, book_id)

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    return book

@app.put("/books/{book_id}")
def update_book(
    book_id: int,
    book: BookCreate,
    db=Depends(get_db)
):
    existing_book = db.get(Book, book_id)

    if not existing_book:
        raise HTTPException(status_code=404, detail="Book not found")

    author = db.get(Author, book.author_id)

    if not author:
        raise HTTPException(status_code=404, detail="Author not found")

    existing_book.title = book.title
    existing_book.author_id = book.author_id

    db.commit()
    db.refresh(existing_book)

    return existing_book


@app.delete("/books/{book_id}")
def delete_book(book_id: int, db=Depends(get_db)):
    book = db.get(Book, book_id)

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    db.delete(book)
    db.commit()

    return {"message": "Book deleted successfully"}


@app.post("/register")
def register_user(user: UserCreate, db=Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    
   
    hash_password = pwd_context.hash(user.password) 
    
    new_user = User(
        username=user.username,
        password=hash_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {
        "id": new_user.id,
        "username": new_user.username
    }
