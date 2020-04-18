import sqlalchemy
import os
import flask
import datetime
from datetime import datetime
from models import *
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine
from flask_session import Session
from flask import Flask, session, render_template, request

# app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")


# app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
# db = SQLAlchemy(app)
# db.init_app(app)


# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
# db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register", methods=["GET"])
def register():
    message = "Hey!! Welcome for Registration"
    return render_template("register.html", message=message)


@app.route("/login", methods=["GET", "POST"])
def login():
    if (request.method == "POST"):
        username = request.form.get("username")
        emailid = request.form.get("emailid")
        password = request.form.get("password")
        gender = request.form.get("gender")
        birthday = str(request.form.get("birthday"))
        now = datetime.now()
        # timestamp = datetime.timestamp(now)
        timestamp = str(now)
        user = User(username=username, email=emailid, password=password,
                    gender=gender, birthday=birthday, timestamp=timestamp)
        db.session.add(user)
        db.session.commit()
    # "{{request.form.get("name")}}"
    return render_template("login.html")


@app.route("/admin")
def admin():
    # details = User.query.all()
    details = User.query.order_by(User.timestamp.asc()).all()
    # stri = User.query.all()
    # conn = engine.connect()
    # resul = conn.execute(stri)
    return render_template("admin.html", userdetails=details)
