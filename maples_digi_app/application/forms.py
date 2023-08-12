from flask_wtf import FlaskForm
from wtforms import DateField, FileField, IntegerField, SelectField, StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError
from maples_digi_app.login.models import Customer


class CustomerForm(FlaskForm):
    """
    Form class to capture and validate customer-related data for application creation.
    This form is used to gather information specific to the Customer table in the database.
    """
    # Add fields specific to the Customer table
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

    def validate_passport_no(self, passport_no):
        existing_customer = Customer.query.filter_by(passport_no=passport_no.data).first()
        if existing_customer:
            raise ValidationError("Passport number is already in use.")


class EmployeeForm(FlaskForm):
    """
    Form class to capture and validate employee-related data for application creation.
    This form is used to gather information specific to the Employee table in the database.
    """
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
