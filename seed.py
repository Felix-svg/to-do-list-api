from config import app, db
from models import Todo

with app.app_context():
    Todo.query.delete()

    todo1 = Todo(task="Learn Flask")
    todo2 = Todo(task="Build a simple API")
    todo3 = Todo(task="Learn C#")

    db.session.add_all([todo1, todo2, todo3])
    db.session.commit()

    print("Seeding complete")
