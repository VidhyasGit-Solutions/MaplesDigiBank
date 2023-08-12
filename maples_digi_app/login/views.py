from datetime import datetime,timedelta
import secrets
from flask import Blueprint, flash, jsonify, redirect, render_template, request, session,url_for
from flask_login import current_user, login_user, logout_user
from loguru import logger
from maples_digi_app.login.forms import LoginForm, ProfileForm, RegisterForm, password_check
from maples_digi_app.login.models import User
from sqlalchemy.exc import IntegrityError
from flask_mail import Message
from maples_digi_app.utils.utils import get_manager_data, send_email
from werkzeug.security import check_password_hash, generate_password_hash
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer
from wtforms.validators import ValidationError
from markupsafe import Markup

logins = Blueprint("logins", __name__)

# Login API
@logins.route("/")
@logins.route("/login", methods=["POST", "GET"])
def login():
    from maples_digi_app import db

    # Create a login form using LoginForm class
    form = LoginForm()

    # Check if the form is submitted and passes validation
    if form.validate_on_submit():
        # Get input values from the form
        username_or_email = form.email.data
        password = form.password.data
        role = form.role_type.data
        session['userrole'] = role
        user = None # Initialize the user as None

        # Check if the input is an email or username and find the user
        if "@" in username_or_email:
            user = User.query.filter_by(
                email=username_or_email, role_type=role
            ).first()
        else:
            user = User.query.filter_by(
                username=username_or_email, role_type=role
            ).first()
        # Check if the user exists
        if user:
            # Check if the user's account is verified
            if user.is_account_verified:
                # Check if the user's account is locked
                if user.account_locked:
                    logger.error(
                        f"{username_or_email} Your account is locked. Please contact support"
                    )
                    flash("Your account is locked. Please contact support.")
                # Validate the entered password
                elif check_password_hash(user.password, password):
                    user.last_login_date = datetime.now()
                    user.reset_failed_login() 
                    db.session.commit()
                    logger.info(f"User {user.username} is  logged in {datetime.now()} successfully.")
                    login_user(user)
                    return redirect("/home")
                else:
                    # Increment failed login attempts and handle locked accounts
                    user.increment_failed_login()
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
                # Display a message for unverified accounts
                flash(
                    "Your account is not verified. Please check your email for activation instructions."
                )
        else:
            # Handle invalid input (username or email)
            logger.error(
                f"Wrong Username or Email entered {username_or_email}. Please try again."
            )
            flash("Invalid Username or Email. Please try again.")
    else:
        # Handle form validation errors
        for field, errors in form.errors.items():
            for error in errors:
                logger.error(f"Validation error for field '{field}': {error}")
    return render_template("login.html", form=form)


# Logout API
@logins.route("/logout", methods=["POST", "GET"])
def logout():
    logger.info(f"current_user is anonymous {current_user.is_anonymous }")
    if not current_user.is_anonymous:
        logger.info(f"User {current_user.username} logged out {datetime.now()} successfully.")
        logout_user()
    return redirect("/login")


# User details API
@logins.route("/users")
def users():
    users = User.query.all()
    result = []
    for user in users:
        res = {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "username": user.username,
            "email": user.email,
            "password": user.password,
            "role_type": user.role_type,
        }
        result.append(res)
    return jsonify(result)


# Profile API
@logins.route("/profile", methods=["GET", "POST"])
def profile():
    from maples_digi_app import db

    form = ProfileForm()
    # Get the current user's information from the database
    user = User.query.filter_by(id=current_user.id).first()

    # Check if the request method is POST (form submission)
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
    # Check if the request method is GET (loading the form)
    elif request.method == "GET":
        # Populate the form fields with the current user's information
        form.first_name.data = user.first_name
        form.last_name.data = user.last_name
        form.username.data = user.username
        form.email.data = user.email
        form.password.data = user.password
        form.role_type.data = user.role_type
        return render_template("profile.html", form=form)


# Route for Registering the User
@logins.route("/register", methods=["POST", "GET"])
def register():
    from maples_digi_app import db, app

    form = RegisterForm()
    # Check if the request method is GET (loading the registration form)
    if request.method == "GET":
        return render_template("register.html", form=form)
    # Check if the request method is POST (form submission)
    if request.method == "POST":
        if form.validate_on_submit():
            try:
                # Create a new user instance with form data
                user = User(
                    first_name=form.first_name.data,
                    last_name=form.last_name.data,
                    username=form.username.data,
                    email=form.email.data,
                    role_type=form.role_type.data,
                    is_account_verified=False,
                    password=generate_password_hash(form.password.data),
                )
                # Add the user to the database and commit changes
                db.session.add(user)
                db.session.commit()
                token_serializer = URLSafeTimedSerializer(
                    app.config["SECRET_KEY"]
                )
                token = token_serializer.dumps(user.email, salt="activate")
                activation_link = url_for(
                    "logins.activate_account", token=token, _external=True
                )
                # Prepare the activation email body and send it
                body = f"Please click the following link to activate your account: {activation_link}"
                logger.debug(body)
                send_email(user.email, body, "Activate Your Account")
                flash(
                    "Activation link is sent to your email. Please activate it",
                    "success",
                )
                return redirect("/login")
            except IntegrityError() as err:
                logger.error(
                    f"IntegrityError occurred while registering the user : {err}"
                )
                flash("Constraint violation: Please check your input.")
        else:
            # Handle form validation errors by logging and displaying them
            for field, errors in form.errors.items():
                for error in errors:
                    logger.error(
                        f"Validation error for field '{field}': {error}"
                    )
            return render_template("register.html", form=form)


# Route for Activating the Account using token
@logins.route("/activate_account/<token>")
def activate_account(token):
    from maples_digi_app import app, db

    try:
        # Deserialize the activation token and extract the email
        token_serializer = URLSafeTimedSerializer(app.config["SECRET_KEY"])
        email = token_serializer.loads(
            token, salt="activate", max_age=3600
        )  # Token valid for 1 hour
    except SignatureExpired:
        flash("Activation link has expired.")
    except BadSignature:
        flash("Invalid activation link.")
    else:
        # Check if the user with the extracted email exists
        user = User.query.filter_by(email=email).first()
        if user:
            user.is_account_verified = True
            db.session.commit()
            # Flash a success message and inform user about account activation
            flash(
                "Your account has been activated. You can now log in.",
                "success",
            )
        else:
            flash("User not found.")
    # Redirect to the login page regardless of the outcome
    return redirect("/login")


# Route for resetting the user's password using a token
@logins.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_password(token):
    from maples_digi_app import db

    # Fetch the user associated with the provided reset token
    user = User.query.filter_by(password_reset_token=token).first()

    # Check if the token is invalid or expired
    if not user or user.password_reset_token_expiration < datetime.now():
        logger.error(f"User {user} Invalid token")
        flash(
            "Invalid or expired token. Please request a new password reset.",
            "error",
        )
        return redirect(url_for("logins.forgot_password"))
    # Handling password reset form submission
    if request.method == "POST":
        new_password = request.form["password"]
        confirm_password = request.form.get("confirm_password")
        errors = password_check(new_password)
        if errors:
            # flash('\n'.join(errors))
            error_message = '<br>'.join(errors)
            flash(Markup(error_message))

            # raise ValidationError(errors)
        else:
            # Check if the new password and confirm password match
            if new_password != confirm_password:
                flash("Passwords do not match. Please try again.", "error")
            else:
                # Update the user's password, reset token, and related data
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


# Route for handling forgot password requests
@logins.route("/forgot_password", methods=["GET", "POST"])
def forgot_password():
    from maples_digi_app import db
    # Handling password reset form submission
    if request.method == "POST":
        email = request.form["email"]
        # Check if the provided email belongs to a registered user
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
    subject = "Password Reset Request"
    msg = Message(
        subject,
        sender="noreply@example.com",
        recipients=[email],
    )
    body = f"Click the link below to reset your password:\n\n{url_for('logins.reset_password', token=token, _external=True)}"
    msg.body = body
    logger.debug(f"Password reset link has been sent to {email}\n {body}")
    # mail.send(msg)
    response = send_email(email, body, subject)
    logger.debug(response)


# Route for retrieving manager options via API
@logins.route("/get_managers", methods=["GET"])
def get_manager_options_api():
    # Fetching manager data from a function
    managers = get_manager_data()
    logger.debug(f"list of all managers {managers}")
    options = []
    # Loop through each manager and create option data
    for each in managers:
        option_data = {}
        option_data["value"] = each.id
        option_data["label"] = each.first_name + each.last_name
        options.append(option_data)

    return jsonify(options)