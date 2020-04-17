import os
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
db.init_app(app)


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    gender = db.Column(db.String, nullable=False)
    birthday = db.Column(db.String, nullable=False)
    timestamp = db.Column(db.String, nullable=False)


def main():
    db.create_all()


if __name__ == "__main__":
    with app.app_context():
        main()

# db.session.add(User(name="Flask", email="example@example.com"))
# db.session.commit()

# users = User.query.all()
