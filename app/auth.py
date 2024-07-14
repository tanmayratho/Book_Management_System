from flask import request, jsonify
from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token
from .models import User
from . import db
from .logger import logger


class UserRegister(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True)
        parser.add_argument('password', type=str, required=True)
        args = parser.parse_args()
        username = args['username']
        password = args['password']
        if not username or not password:
            logger.error('Missing username or password')
            return jsonify({"msg": "Missing username or password"}), 400
        if User.query.filter_by(username=username).first():
            logger.error('Username already exists')
            return jsonify({"msg": "Username already exists"}), 400

        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        logger.info(f"User {args['username']} registered successfully")
        return jsonify({"msg": "User registered successfully"}), 201


class UserLogin(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True)
        parser.add_argument('password', type=str, required=True)
        args = parser.parse_args()
        username = args['username']
        password = args['password']
        if not username or not password:
            logger.error('Missing username or password')
            return jsonify({"msg": "Missing username or password"}), 400

        user = User.query.filter_by(username=username).first()
        if user is None or not user.check_password(password):
            logger.error('Invalid username or password')
            return jsonify({"msg": "Invalid username or password"}), 401

        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
