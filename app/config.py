import os


class Config:
    DATABASE_URI = 'postgresql+asyncpg://postgres:postgres@123@localhost:5432/book_management_system'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    SECRET_KEY = os.getenv('SECRET_KEY')
