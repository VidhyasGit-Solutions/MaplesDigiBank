from datetime import datetime

from flask import Blueprint, flash, jsonify, redirect, render_template, request
from flask_login import current_user, login_user, logout_user
from loguru import logger
from maples_digi_app.login.forms import LoginForm, ProfileForm, RegisterForm
from maples_digi_app.login.models import User
from sqlalchemy.exc import IntegrityError
from werkzeug.security import check_password_hash, generate_password_hash

logins = Blueprint("logins", __name__)


@logins.route("/")
@logins.route("/login", methods=["POST", "GET"])
def login():
    from maples_digi_app import db

    form = LoginForm()
    if form.validate_on_submit():

        username_or_email = form.email.data
        password = form.password.data
        role = form.role_type.data
        user = None
        if "@" in username_or_email:
            user = User.query.filter_by(
                email=username_or_email, role_type=role
            ).first()
        else:
            user = User.query.filter_by(
                username=username_or_email, role_type=role
            ).first()
        if user:
            if check_password_hash(user.password, password):
                user.last_login_date = datetime.now()
                db.session.commit()
                logger.info(f"User {user.username} is  logged in {datetime.now()} successfully.")
                login_user(user)
                return redirect("/home")
            else:
                logger.error(
                    f"Wrong password entered for {username_or_email}. Please try again."
                )
                flash("Wrong password. Please try again.")
        else:
            logger.error(
                f"Wrong Username or Email entered {username_or_email}. Please try again."
            )
            flash("Invalid Username or Email. Please try again.")
    else:
        for field, errors in form.errors.items():
            for error in errors:
                logger.error(f"Validation error for field '{field}': {error}")
    return render_template("login.html", form=form)


@logins.route("/logout", methods=["POST", "GET"])
def logout():
    logger.info(f"User {current_user.username} logged out {datetime.now()} successfully.")

    logout_user()
    return redirect("/login")


@logins.route("/users")
def users():
    users = User.query.all()
    res = {}
    for user in users:
        res = {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "username": user.username,
            "email": user.email,
            "password": user.password,
            "role_type": user.role_type,
        }
    return jsonify(res)


@logins.route("/profile", methods=["GET", "POST"])
def profile():
    from maples_digi_app import db

    form = ProfileForm()
    user = User.query.filter_by(id=current_user.id).first()
    if request.method == "POST":
        if form.validate_on_submit():
            user.username = form.username.data
            if form.password.data:
                user.password = generate_password_hash(form.password.data)
            db.session.commit()
            return redirect("/applications")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    logger.error(
                        f"Validation error for field '{field}': {error}"
                    )

    elif request.method == "GET":
        form.first_name.data = user.first_name
        form.last_name.data = user.last_name
        form.username.data = user.username
        form.email.data = user.email
        form.password.data = user.password
        form.role_type.data = user.role_type
        return render_template("profile.html", form=form)


@logins.route("/register", methods=["POST", "GET"])
def register():
    from maples_digi_app import db

    form = RegisterForm()
    if request.method == "GET":
        return render_template("register.html", form=form)

    if request.method == "POST":
        if form.validate_on_submit():
            try:
                user = User(
                    first_name=form.first_name.data,
                    last_name=form.last_name.data,
                    username=form.username.data,
                    email=form.email.data,
                    role_type=form.role_type.data,
                    password=generate_password_hash(form.password.data),
                )
                db.session.add(user)
                db.session.commit()
                return redirect("/login")
            except IntegrityError() as err:
                logger.error(
                    f"IntegrityError occurred while registering the user : {err}"
                )
                flash("Constraint violation: Please check your input.")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    logger.error(
                        f"Validation error for field '{field}': {error}"
                    )
            return render_template("register.html", form=form)
