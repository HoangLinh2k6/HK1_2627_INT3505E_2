from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, Text, ForeignKey, Column, Table
from sqlalchemy.orm import mapped_column, relationship

db = SQLAlchemy()

book_authors = Table(
    'book_authors',
    db.metadata,
    Column('book_id', Integer, ForeignKey('books.id'), primary_key=True),
    Column('author_id', Integer, ForeignKey('authors.id'), primary_key=True)
)

class Book(db.Model):
    __tablename__ = 'books'

    id = mapped_column(Integer, primary_key=True)
    title = mapped_column(String(200), nullable=False)
    isbn = mapped_column(String(13), unique=True)
    price_vnd = mapped_column(Integer)
    stock = mapped_column(Integer, default=0)
    
    category_id = mapped_column(ForeignKey("categories.id"))
    category = relationship("Category", back_populates="books")
    
    authors = relationship("Author", secondary=book_authors, back_populates="books")

    def to_dict(self):
        return {
            "id": f"book_{self.id}",
            "title": self.title,
            "isbn": self.isbn,
            "price_vnd": self.price_vnd,
            "stock": self.stock,
            "category": self.category.name if self.category else None,
            "authors": [a.name for a in self.authors]
        }

class Author(db.Model):
    __tablename__ = 'authors'

    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(100), nullable=False)
    bio = mapped_column(Text)
    
    books = relationship("Book", secondary=book_authors, back_populates="authors")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "bio": self.bio
        }
    
class Category(db.Model):
    __tablename__ = 'categories'
    
    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(100), nullable=False)
    slug = mapped_column(String(100), unique=True)
    books = relationship("Book", back_populates="category")

class Review(db.Model):
    __tablename__ = 'reviews'

    id = mapped_column(Integer, primary_key=True)
    content = mapped_column(Text, nullable=False)
    rating = mapped_column(Integer, nullable=False)
    
    book_id = mapped_column(ForeignKey("books.id"))
    user_id = mapped_column(ForeignKey("users.id"))
    
    book = relationship("Book", back_populates="reviews")
    user = relationship("User", back_populates="reviews")

    def to_dict(self):
        return {
            "id": self.id,
            "content": self.content,
            "rating": self.rating,
            "book_id": self.book_id,
            "user_id": self.user_id
        }
    
class User(db.Model):
    __tablename__ = 'users'

    id = mapped_column(Integer, primary_key=True)
    display_name = mapped_column(String(100))
    email = mapped_column(String(100), unique=True, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "display_name": self.display_name,
            "email": self.email
        }