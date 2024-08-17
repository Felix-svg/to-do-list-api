from flask import request, make_response
from flask_restful import Resource
from models import Todo
from utils import (
    server_error,
    no_input,
    missing_required_fields,
    created,
    not_found,
    updated,
    deleted,
)
from config import db


class Todos(Resource):
    def get(self):
        try:
            todos = [todo.to_dict() for todo in Todo.query.all()]
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
    def get(self, id):
        try:
            todo = Todo.query.filter(Todo.id == id).first()
            if not todo:
                return not_found("Task")
            todo_dict = todo.to_dict()
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
            db.session.rollback()
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
