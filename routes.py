from flask import request, make_response
from flask_restful import Resource
from models import Todo, User, Tokenblocklist
from utils import (
    server_error,
    no_input,
    missing_required_fields,
    created,
    not_found,
    updated,
    deleted,
)
from config import db, jwt
from flask_jwt_extended import (
    get_jwt,
    jwt_required,
    get_jwt_identity,
)
from datetime import timedelta, datetime, timezone


class Index(Resource):
    def get(self):
        return make_response({"message": "Home"}, 200)


class Users(Resource):
    def get(self):
        try:
            users = [user.to_dict(only=("email", "name")) for user in User.query.all()]
            return make_response(users, 200)
        except Exception as e:
            return server_error(e)

    def post(self):
        try:
            data = request.get_json()
            if not data:
                return no_input()

            name = data.get("name")
            email = data.get("email")
            password = data.get("password")

            if not name or not email or not password:
                return missing_required_fields()

            if User.query.filter(User.email == email).first():
                return make_response({"message": "Email already exists"}, 400)

            new_user = User(name=name, email=email)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            return created("User")
        except Exception as e:
            db.session.rollback()
            return server_error(e)


class UserByID(Resource):
    def get(self, id):
        try:
            # user = User.query.filter(User.id == id).first_or_404(description="User not found")
            user = User.query.filter(User.id == id).first()
            if not user:
                return not_found("User")

            user_dict = user.to_dict(only=("name", "email", "id"))
            return make_response(user_dict, 200)
        except Exception as e:
            return server_error(e)

    def patch(self, id):
        try:
            user = User.query.filter(User.id == id).first()
            if not user:
                return not_found("User")

            data = request.get_json()
            if not data:
                return no_input()

            name = data.get("name")
            email = data.get("email")
            password = data.get("password")

            if name is not None:
                user.name = name
            if email is not None:
                user.email = email
            if password is not None:
                user.set_password(password)

            db.session.commit()
            return updated("User")
        except Exception as e:
            db.session.rollback()
            return server_error(e)

    def delete(self, id):
        try:

            user = User.query.filter(User.id == id).first()
            if not user:
                return not_found("User")

            db.session.delete(user)
            db.session.commit()
            return deleted("User")
        except Exception as e:
            db.session.rollback()
            return server_error(e)


class Todos(Resource):
    @jwt_required()
    def get(self):
        try:
            user_id = get_jwt_identity()
            todos = [
                todo.to_dict(rules=["-user"])
                for todo in Todo.query.filter_by(user_id=user_id).all()
            ]
            return make_response(todos, 200)
        except Exception as e:
            return server_error(e)

    def post(self):
        try:
            data = request.get_json()
            if not data:
                return no_input()
            task = data.get("task")
            if not task:
                return missing_required_fields()

            new_todo = Todo(task=task)
            db.session.add(new_todo)
            db.session.commit()
            return created("Task")
        except Exception as e:
            db.session.rollback()
            return server_error(e)


class TodoByID(Resource):
    @jwt_required()
    def get(self, id):
        try:
            todo = Todo.query.filter(Todo.id == id).first()
            if not todo:
                return not_found("Task")
            todo_dict = todo.to_dict(rules=["-user"])
            return make_response(todo_dict, 200)
        except Exception as e:
            return server_error(e)

    def patch(self, id):
        try:
            todo = Todo.query.filter(Todo.id == id).first()
            if not todo:
                return not_found("Task")

            data = request.get_json()
            if not data:
                return no_input()

            task = data.get("task")
            completed = data.get("completed")
            if task is not None:
                todo.task = task

            if completed is not None:
                todo.completed = completed

            db.session.commit()
            return updated("Task")
        except Exception as e:
            db.session.rollback(e)
            return server_error()

    def delete(self, id):
        try:
            todo = Todo.query.filter(Todo.id == id).first()
            if not todo:
                return not_found("Task")

            db.session.delete(todo)
            db.session.commit()
            return deleted("Task")
        except Exception as e:
            db.session.rollback()
            return server_error(e)


class Login(Resource):
    def post(self):
        try:
            data = request.get_json()
            if not data:
                return no_input()

            email = data.get("email")
            password = data.get("password")

            if not email or not password:
                return missing_required_fields()

            user = User.query.filter_by(email=email).first()
            if not user or not user.check_password(password):
                return make_response({"message": "Invalid credentials"}, 401)

            token = user.get_token(expires_in=timedelta(hours=1))
            return make_response({"token": token}, 200)
        except Exception as e:
            db.session.rollback()
            return server_error(e)


class Logout(Resource):
    @jwt_required()
    def post(self):
        try:
            jti = get_jwt()["jti"]
            token_block = Tokenblocklist(jti=jti, created_at=datetime.now(timezone.utc))
            db.session.add(token_block)
            db.session.commit()
            return make_response({"messagge": "Successfully logged out"}, 200)
        except Exception as e:
            db.session.rollback()
            return server_error(e)
