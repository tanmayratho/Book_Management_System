from flask import request, jsonify
from flask_restful import Api, Resource
from .models import Book, Review
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from flask_jwt_extended import jwt_required
from .logger import logger
import asyncio
from .config import Config

DATABASE_URL = Config.DATABASE_URI
engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


class Book(Resource):
    @jwt_required()
    async def get(self, book_id):
        async with SessionLocal() as session:
            result = await session.execute(select(Book).where(Book.id == book_id))
            book = result.scalars().first()
            if book is None:
                logger.error(f"Book {book_id} not found")
                return {"message": "Book not found"}, 404
            logger.info(f"Retrieved book {book_id}")
            return {
                "id": book.id,
                "title": book.title,
                "author": book.author,
                "genre": book.genre,
                "year_published": book.year_published
            }

    @jwt_required()
    async def put(self, book_id):
        data = request.json
        async with SessionLocal() as session:
            book = await session.get(Book, book_id)
            if book is None:
                logger.error(f"Book {book_id} not found")
                return {"message": "Book not found"}, 404
            book.title = data['title']
            book.author = data['author']
            book.genre = data['genre']
            book.year_published = data['year_published']
            await session.commit()
            logger.info(f"Updated book {book_id}")
            return {
                "id": book.id,
                "title": book.title,
                "author": book.author,
                "genre": book.genre,
                "year_published": book.year_published
            }

    @jwt_required()
    async def delete(self, book_id):
        async with SessionLocal() as session:
            book = await session.get(Book, book_id)
            if book is None:
                logger.error(f"Book {book_id} not found")
                return {"message": "Book not found"}, 404
            await session.delete(book)
            await session.commit()
            logger.info(f"Deleted book {book_id}")
            return {"message": "Book deleted"}, 204


class BookList(Resource):
    @jwt_required()
    async def get(self):
        async with SessionLocal() as session:
            result = await session.execute(select(Book))
            books = result.scalars().all()
            logger.info("Retrieved all books")
            return [{
                "id": book.id,
                "title": book.title,
                "author": book.author,
                "genre": book.genre,
                "year_published": book.year_published
            } for book in books]

    @jwt_required()
    async def post(self):
        data = request.json
        new_book = Book(
            title=data['title'],
            author=data['author'],
            genre=data['genre'],
            year_published=data['year_published'],
            summary=data['summary']
        )
        async with SessionLocal() as session:
            session.add(new_book)
            await session.commit()
            logger.info(f"Created new book {new_book.id}")
            return {
                "id": new_book.id,
                "title": new_book.title,
                "author": new_book.author,
                "genre": new_book.genre,
                "year_published": new_book.year_published
            }, 201


class Review(Resource):
    @jwt_required()
    async def post(self, book_id):
        data = request.json
        new_review = Review(
            book_id=book_id,
            user_id=data['user_id'],
            review_text=data['review_text'],
            rating=data['rating']
        )
        async with SessionLocal() as session:
            session.add(new_review)
            await session.commit()
            logger.info(f"Added review {new_review.id} for book {book_id}")
            return {
                "id": new_review.id,
                "book_id": new_review.book_id,
                "user_id": new_review.user_id,
                "review_text": new_review.review_text,
                "rating": new_review.rating
            }, 201

    @jwt_required()
    async def get(self, book_id):
        async with SessionLocal() as session:
            result = await session.execute(select(Review).where(Review.book_id == book_id))
            reviews = result.scalars().all()
            logger.info(f"Retrieved reviews for book {book_id}")
            return [{
                "id": review.id,
                "book_id": review.book_id,
                "user_id": review.user_id,
                "review_text": review.review_text,
                "rating": review.rating
            } for review in reviews]

