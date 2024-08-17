from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from flask_restful import Api
from flask_migrate import Migrate

app = Flask(__name__)

app.config["SECRET_KEY"] = (
    "d5615a3262708ca32d44455e0a3a24cdbd0627cac4d7887f3e4d390a50dda89f"
)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todos.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

metadata = MetaData()
db = SQLAlchemy(metadata=metadata)
db.init_app(app)
migrate = Migrate(app, db)

api = Api(app)
