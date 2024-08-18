from config import app, api, jwt
from routes import Todos, TodoByID, Users, UserByID, Index, Login, Logout
from models import Tokenblocklist


@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    token = Tokenblocklist.query.filter_by(jti=jti).first()
    return token is not None


# routes
api.add_resource(Index, "/api/")
api.add_resource(Users, "/api/users/")
api.add_resource(UserByID, "/api/users/<int:id>/")
api.add_resource(Todos, "/api/todos/")
api.add_resource(TodoByID, "/api/todos/<int:id>/")
api.add_resource(Login, "/api/login/")
api.add_resource(Logout, "/api/logout/")


if __name__ == "__main__":
    app.run(debug=True)
