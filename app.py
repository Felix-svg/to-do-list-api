from config import app, api
from routes import Todos, TodoByID, Users, UserByID, Index

# routes
api.add_resource(Index, "/api/")
api.add_resource(Users, "/api/users/")
api.add_resource(UserByID, "/api/users/<int:id>/")
api.add_resource(Todos, "/api/todos/")
api.add_resource(TodoByID, "/api/todos/<int:id>/")


if __name__ == "__main__":
    app.run(debug=True)
