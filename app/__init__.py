from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from .config import Config
from .logger import logger

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    api = Api(app)

    from .auth import UserRegister, UserLogin
    from .routes import BookList, Book, Review

    api.add_resource(UserRegister, '/register')
    api.add_resource(UserLogin, '/login')
    api.add_resource(BookList, '/books')
    api.add_resource(Book, '/books/<int:book_id>')
    api.add_resource(Review, '/books/<int:book_id>/reviews')

    with app.app_context():
        from . import routes, auth
        db.create_all()

    return app
