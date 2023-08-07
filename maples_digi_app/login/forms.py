from flask_wtf import FlaskForm
from maples_digi_app.login.models import User
from wtforms import BooleanField, EmailField, PasswordField, SelectField, StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError


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

    def validate_email(self, email):
        existing_user = User().query.filter_by(email=email.data).first()
        if existing_user:
            raise ValidationError(
                "Email already exists. Please choose a different email."
            )
        
    def validate_username(self, username):
        existing_user = User().query.filter_by(username=username.data).first()
        if existing_user:
            raise ValidationError(
                "Username already exists. Please choose a different username."
            )


    def validate_password(self, password):
        if len(password.data) < 8:
            raise ValidationError(
                "Password must be at least 8 characters long."
            )


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

    def validate_email(self, email):
        existing_user = User().query.filter_by(email=email.data).first()
        if existing_user:
            raise ValidationError(
                "Email already exists. Please choose a different email."
            )
