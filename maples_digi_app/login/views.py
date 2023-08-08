from datetime import datetime,timedelta
import secrets
from flask import Blueprint, flash, jsonify, redirect, render_template, request, session,url_for
from flask_login import current_user, login_user, logout_user
from loguru import logger
from maples_digi_app.login.forms import LoginForm, ProfileForm, RegisterForm
from maples_digi_app.login.models import User
from sqlalchemy.exc import IntegrityError
from flask_mail import Message
from maples_digi_app.utils.utils import get_manager_data
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
        session['userrole'] = role
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
            if user.account_locked:
                logger.error(
                    f"{username_or_email} Your account is locked. Please contact support"
                )
                flash("Your account is locked. Please contact support.")
            elif check_password_hash(user.password, password):
                user.last_login_date = datetime.now()
                user.reset_failed_login() 
                
                db.session.commit()
                logger.info(f"User {user.username} is  logged in {datetime.now()} successfully.")
                login_user(user)
                return redirect("/home")
            else:
                user.increment_failed_login()  # Increment failed login attempts
                db.session.commit()
                if user.failed_login_attempt >= 3:
                    user.account_locked = True  # Lock the account after 3 failed attempts
                    db.session.commit()
                    logger.warning(f"User {user.username}'s account locked due to multiple failed attempts.")
                    flash("Your account has been locked due to multiple failed attempts. Please contact support.")
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
    logger.info(f"current_user is anonymous {current_user.is_anonymous }")
    if not current_user.is_anonymous:
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

# Password reset route
@logins.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_password(token):
    from maples_digi_app import db

    user = User.query.filter_by(password_reset_token=token).first()

    if not user or user.password_reset_token_expiration < datetime.now():
        logger.error(f"User {user} Invalid token")
        flash(
            "Invalid or expired token. Please request a new password reset.",
            "error",
        )
        return redirect(url_for("logins.forgot_password"))
    if request.method == "POST":
        new_password = request.form["password"]
        confirm_password = request.form.get("confirm_password")

        if new_password != confirm_password:
            flash("Passwords do not match. Please try again.", "error")
        else:
            user.password = generate_password_hash(new_password)
            user.password_reset_token = None
            user.password_reset_token_expiration = None
            user.reset_failed_login()
            db.session.commit()
            logger.debug(f"User {user.username} password reset successfully.")
            flash(
                "Your password has been successfully reset. You can now log in with your new password.",
                "success",
            )
            return redirect(url_for("logins.login"))
    logger.debug(f"token {token} is being used to reset password")
    return render_template("reset_password.html", token=token)


@logins.route("/forgot_password", methods=["GET", "POST"])
def forgot_password():
    from maples_digi_app import db

    if request.method == "POST":
        email = request.form["email"]
        user = User.query.filter_by(email=email).first()
        if user:
            # Generate a unique token
            token = secrets.token_hex(16)
            user.password_reset_token = token
            user.password_reset_token_expiration = datetime.now() + timedelta(
                hours=1
            )
            db.session.commit()

            flash(
                "An email with instructions to reset your password has been sent to your email address.",
                "success",
            )

            # Send the token to the user's email
            send_password_reset_email(email, token)
            logger.debug(
                f"password reset link has been sent to your email {email}"
            )
            return redirect("/login")
        else:
            logger.debug(f"Invalid email address {email}. Please try again.")
            flash("Invalid email address. Please try again.", "error")
    return render_template("forgot_password.html")


# Helper function to send password reset email
def send_password_reset_email(email, token):
    msg = Message(
        "Password Reset Request",
        sender="noreply@example.com",
        recipients=[email],
    )
    msg.body = f"Click the link below to reset your password:\n\n{url_for('logins.reset_password', token=token, _external=True)}"
    logger.debug(
        f"Click the link below to reset your password:\n\n{url_for('logins.reset_password', token=token, _external=True)}"
    )

    logger.debug(f"Password reset link has been sent to {email}")
    # mail.send(msg)

@logins.route("/get_managers", methods=["GET"])
def get_manager_options_api():
    managers = get_manager_data()
    logger.debug(f"list of all managers {managers}")
    options = []
    for each in managers:
        option_data = {}
        option_data["value"] = each.id
        option_data["label"] = each.first_name + each.last_name
        options.append(option_data)

    return jsonify(options)