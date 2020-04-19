import sqlalchemy
import os
import flask
import datetime
from datetime import datetime
from models import *
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine
from flask_session import Session
from flask import Flask, session, render_template, request, redirect, url_for, flash, get_flashed_messages

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
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    message = "Hey Deep Reader, Welcome Back !!"
    if (request.method == "POST"):
        username = request.form.get("username")
        emailid = request.form.get("emailid")
        password = request.form.get("password")
        gender = request.form.get("gender")
        birthday = str(request.form.get("birthday"))
        now = datetime.now()
        sampleuser = User.query.filter(User.username == username).all()
        sampleemail = User.query.filter(User.email == emailid).all()
        # app.logger.info(len(sampleuser))
        if (len(sampleuser) != 0):
            message = "This User Name already exists, Please Log IN"
        elif (len(sampleemail) != 0):
            message = "This Email ID already exists, Please Log IN"
        else:
            # timestamp = datetime.timestamp(now)
            message = "Registration was success, Please Log IN"
            timestamp = str(now)
            user = User(username=username, email=emailid, password=password,
                        gender=gender, birthday=birthday, timestamp=timestamp)
            db.session.add(user)
            db.session.commit()
    # "{{request.form.get("name")}}"
    return render_template("login.html", message=message)


@app.route("/logout")
def logout():
    session.pop("USERNAME", None)
    return redirect(url_for("login"))


@app.route("/authentication", methods=["POST"])
def authentication():
    username = request.form.get("username")
    password = request.form.get("password")
    sampleuser = User.query.filter(User.username == username).all()
    # app.logger.info(sampleuser)
    if (len(sampleuser) == 0):
        # message = "This User Name Doesn't exist, Please Sign UP"
        flash("This User Name Doesn't exist, Please Sign UP")
        return redirect(url_for('register'))
    else:
        if (sampleuser[0].password != password):
            flash("Please enter correct Password")
            return redirect(url_for('login'))
        else:
            session["USERNAME"] = str(sampleuser[0].username)
            return redirect(url_for("user"))
            # return render_template("user.html")


@app.route("/user")
def user():
    if not session.get("USERNAME") is None:
        username = session.get("USERNAME")
        return render_template("user.html", user=username)
    else:
        return redirect(url_for("login"))


@app.route("/admin")
def admin():
    # details = User.query.all()
    details = User.query.order_by(User.timestamp.asc()).all()
    # sample1 = User.query.filter(User.username == "Deep").all()
    # sample2 = User.query.filter(User.username == "Deepp").all()
    # app.logger.info("sample1")
    # app.logger.info(len(sample1))
    # app.logger.info("sample2")
    # app.logger.info(len(sample2))
    return render_template("admin.html", userdetails=details)
