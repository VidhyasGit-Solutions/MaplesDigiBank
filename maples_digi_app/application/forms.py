from flask_wtf import FlaskForm
from wtforms import DateField, FileField, IntegerField, SelectField, StringField, SubmitField
from wtforms.validators import DataRequired

# from wtforms.validators import ValidationError


class CustomerForm(FlaskForm):
    passport_no = StringField(
        "Passport Number",
        validators=[DataRequired()],
        render_kw={"placeholder": "Enter your Passport Number"},
    )
    first_name = StringField(
        "First Name",
        render_kw={"placeholder": "Enter your First Name"},
        validators=[DataRequired()],
    )
    middle_name = StringField(
        "Middle Name", render_kw={"placeholder": "Enter your Last Name"}
    )
    last_name = StringField(
        "Last Name",
        render_kw={"placeholder": "Enter your Last Name"},
        validators=[DataRequired()],
    )
    sin = StringField("Social Insurance Number")

    date_of_birth = DateField(
        "Date of Birth", format="%Y-%m-%d", validators=[DataRequired()]
    )

    address_line1 = StringField("Address Line 1", validators=[DataRequired()])
    address_line2 = StringField("Address Line 2")
    city = StringField("City", validators=[DataRequired()])
    province = StringField("Province", validators=[DataRequired()])
    postal_code = StringField("Postal Code", validators=[DataRequired()])
    country = StringField("Country", validators=[DataRequired()])
    mobile_no = IntegerField("Phone Number", validators=[DataRequired()])
    nationality = StringField("Nationality", validators=[DataRequired()])
    account_type = StringField("Account Type", validators=[DataRequired()])

    occupation = StringField("Occupation", validators=[DataRequired()])
    application_id = IntegerField("Application ID")
    passport_file_name = StringField("Uploaded File name")
    passport_file = FileField("Upload Passport (PDF or Image)")
    signature = FileField("Signature", validators=[DataRequired()])
    submitted_on = DateField(
        "Submitted On", format="%Y-%m-%d", validators=[DataRequired()]
    )
    submit = SubmitField("Create Application")

    # def validate_email(self, email):
    #     existing_user = User().query.filter_by(email=email.data).first()
    #     if existing_user:
    #         raise ValidationError(
    #             "Email already exists. Please choose a different email."
    #         )

    # def validate_password(self, password):
    #     if len(password.data) < 8:
    #         raise ValidationError(
    #             "Password must be at least 8 characters long."
    #         )


class EmployeeForm(FlaskForm):
    # Add fields specific to the Employee table
    first_name = StringField(
        "First Name",
        render_kw={"placeholder": "Enter your First Name"},
        validators=[DataRequired()],
    )
    middle_name = StringField(
        "Middle Name", render_kw={"placeholder": "Enter your Last Name"}
    )
    last_name = StringField(
        "Last Name",
        render_kw={"placeholder": "Enter your Last Name"},
        validators=[DataRequired()],
    )
    # employee_id = IntegerField("Employee ID", validators=[DataRequired()])
    date_of_joining = DateField(
        "Date of Joining", format="%Y-%m-%d", validators=[DataRequired()]
    )
    institution_no = StringField("Institution Number")
    designation = StringField("Designation", validators=[DataRequired()])
    date_of_birth = DateField(
        "Date of Birth", format="%Y-%m-%d", validators=[DataRequired()]
    )
    # auth_to_approve = SelectField(
    #     "Authorization to Approve",
    #     choices=[("Yes", "Yes"), ("No", "No")],
    #     validators=[DataRequired()],
    # )
    manager_id = IntegerField("Manager ID")
    address_line1 = StringField("Address Line 1", validators=[DataRequired()])
    address_line2 = StringField("Address Line 2")
    city = StringField("City", validators=[DataRequired()])
    province = StringField("Province", validators=[DataRequired()])
    postal_code = StringField("Postal Code", validators=[DataRequired()])
    country = StringField("Country", validators=[DataRequired()])
    mobile_no = IntegerField("Phone Number", validators=[DataRequired()])
    nationality = StringField("Nationality", validators=[DataRequired()])
    signature = FileField("Signature", validators=[DataRequired()])

    submit = SubmitField("Create Application")
