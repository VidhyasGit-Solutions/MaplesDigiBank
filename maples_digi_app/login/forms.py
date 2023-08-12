import re

from flask_wtf import FlaskForm
from maples_digi_app.login.models import User
from wtforms import BooleanField, EmailField, PasswordField, SelectField, StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError


def password_check(password):
    errors = []
    if len(password) < 8:
        errors.append("Password must be at least 8 characters long.")
    if not re.search(r"[A-Z]", password):
        errors.append("Password must contain at least one Uppercase letter.")
    if not re.search(r"[!@#$%^&*()\-_=+{}[\]:;,.<>?/\\]", password):
        errors.append("Password must contain at least one Special character.")
    if not re.search(r"\d", password):
        errors.append("Password must contain at least one Number.")
    return errors


class RegisterForm(FlaskForm):
    first_name = StringField(
        "First Name",
        validators=[DataRequired()],
        render_kw={"placeholder": "Enter your First Name"},
    )
    last_name = StringField(
        "Last Name",
        validators=[DataRequired()],
        render_kw={"placeholder": "Enter your Last Name"},
    )
    username = StringField(
        "Username",
        validators=[DataRequired()],
        render_kw={"placeholder": "Enter your Username"},
    )
    email = EmailField(
        "Email",
        validators=[DataRequired()],
        render_kw={"placeholder": "Enter your Email"},
    )
    password = PasswordField(
        "Password",
        validators=[DataRequired()],
        render_kw={"placeholder": "Enter your Password"},
    )
    role_type = SelectField(
        "Role",
        choices=[("customer", "Customer"), ("employee", "Employee")],
        validators=[DataRequired()],
    )
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Register")

    def validate_empty_or_whitespace(self, field):
        if field.data.strip() == "":
            raise ValidationError(
                f"{field.label.text} cannot be empty or contain only spaces."
            )

    def validate_special_characters(self, field):
        if re.search(r"[#@\$]", field.data):
            raise ValidationError(
                f"{field.label.text} cannot contain special characters like '#', '@', or '$'."
            )

    def validate_only_letters(self, field):
        if not re.match(r"^[A-Za-z]*$", field.data):
            raise ValidationError(
                f"{field.label.text} should only contain letters."
            )

    def validate_only_letters_and_space(self, field):
        if not re.match(r"^[A-Za-z\s]*$", field.data):
            raise ValidationError(
                f"{field.label.text} should only contain letters."
            )

    def validate_first_name(self, first_name):
        self.validate_empty_or_whitespace(first_name)
        self.validate_only_letters(first_name)

    def validate_last_name(self, last_name):
        self.validate_empty_or_whitespace(last_name)
        self.validate_only_letters_and_space(last_name)

    def validate_email(self, email):
        existing_user = User().query.filter_by(email=email.data).first()
        if existing_user:
            raise ValidationError(
                "Email already exists. Please choose a different email."
            )

    def validate_username(self, username):
        self.validate_empty_or_whitespace(username)
        self.validate_special_characters(username)
        existing_user = User().query.filter_by(username=username.data).first()
        if existing_user:
            raise ValidationError(
                "Username already exists. Please choose a different username."
            )

    def validate_password(self, password):
        errors = password_check(password.data)
        if errors:
            raise ValidationError(errors)


class LoginForm(FlaskForm):
    email = StringField(
        "Email / Username:",
        validators=[DataRequired()],
        render_kw={"placeholder": "Enter your Username or Email"},
    )
    password = PasswordField(
        "Password:",
        validators=[DataRequired()],
        render_kw={"placeholder": "Enter your Password"},
    )
    role_type = SelectField(
        "Login As:",
        choices=[("customer", "Customer"), ("employee", "Employee")],
        validators=[DataRequired()],
    )
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Login")


class ProfileForm(FlaskForm):
    first_name = StringField("First Name")
    last_name = StringField("Last Name")
    username = StringField("Username", validators=[DataRequired()])
    email = EmailField("Email")
    password = PasswordField("Password")
    role_type = StringField("Role")
    remember_me = BooleanField("Remember Me")
    submit = SubmitField(label=("Update"))

    def validate_empty_or_whitespace(self, field):
        if field.data.strip() == "":
            raise ValidationError(
                f"{field.label.text} cannot be empty or contain only spaces."
            )

    def validate_special_characters(self, field):
        if re.search(r"[#@\$]", field.data):
            raise ValidationError(
                f"{field.label.text} cannot contain special characters like '#', '@', or '$'."
            )

    def validate_only_letters(self, field):
        if not re.match(r"^[A-Za-z]*$", field.data):
            raise ValidationError(
                f"{field.label.text} should only contain letters."
            )

    def validate_only_letters_and_space(self, field):
        if not re.match(r"^[A-Za-z\s]*$", field.data):
            raise ValidationError(
                f"{field.label.text} should only contain letters."
            )

    def validate_first_name(self, first_name):
        self.validate_empty_or_whitespace(first_name)
        self.validate_only_letters(first_name)

    def validate_last_name(self, last_name):
        self.validate_empty_or_whitespace(last_name)
        self.validate_only_letters_and_space(last_name)

    def validate_email(self, email):
        existing_user = User().query.filter_by(email=email.data).first()
        if existing_user:
            raise ValidationError(
                "Email already exists. Please choose a different email."
            )

    def validate_username(self, username):
        self.validate_empty_or_whitespace(username)
        self.validate_special_characters(username)
        existing_user = User().query.filter_by(username=username.data).first()
        if existing_user:
            raise ValidationError(
                "Username already exists. Please choose a different username."
            )

    def validate_password(self, password):
        errors = password_check(password.data)
        if errors:
            raise ValidationError(errors)
