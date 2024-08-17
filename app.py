from config import app, api
from routes import Todos, TodoByID

# routes
api.add_resource(Todos, "/todos")
api.add_resource(TodoByID, "/todos/<int:id>")


if __name__ == "__main__":
    app.run(debug=True)
