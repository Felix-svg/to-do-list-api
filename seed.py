from config import app, db
from models import Todo, User

with app.app_context():
    Todo.query.delete()
    User.query.delete()

    user1 = User(name="Jon Doe", email="jondoe@email.com")
    user1.set_password("1234")
    user2 = User(name="Jane Doe", email="janedoe@email.com")
    user2.set_password("5678")

    db.session.add_all([user1, user2])
    db.session.commit()

    todo1 = Todo(task="Learn Flask", user_id=user1.id)
    todo2 = Todo(task="Build a simple API", user_id=user2.id)
    todo3 = Todo(task="Learn C#", user_id=user1.id)

    db.session.add_all([todo1, todo2, todo3])
    db.session.commit()

    print("Seeding complete")
