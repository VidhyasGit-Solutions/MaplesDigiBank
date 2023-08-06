from flask_wtf import FlaskForm
from wtforms import DateField, FileField, IntegerField, SelectField, StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError
from maples_digi_app.login.models import Customer

# from wtforms.validators import ValidationError

class CreditCheck_CustomerForm(FlaskForm):
    full_name = StringField(
        "Full Legal Name",
        render_kw={"placeholder": "Enter your Full Legal Name"},
        validators=[DataRequired()],
    )
    
    date_of_birth = DateField(
        "Date of Birth", format="%Y-%m-%d",
        render_kw={"placeholder": "Enter your Date of Birth"},
        validators=[DataRequired()]
    )

    nin = StringField("National Identification Number",
        render_kw={"placeholder": "Enter your National Identification Number"},
        validators=[DataRequired()]
    )
    email = StringField("Email",
        render_kw={"placeholder": "Enter your Email"},
        validators=[DataRequired()]
    )
    address_line1 = StringField("Address Line 1", 
        render_kw={"placeholder": "Enter your Address"},
        validators=[DataRequired()]
    )
    address_line2 = StringField("Address Line 2",
         render_kw={"placeholder": "Enter your Address"},
         validators=[DataRequired()]
    )
    city = StringField("City",
         render_kw={"placeholder": "Enter your City"},
         validators=[DataRequired()]
    )
    province = StringField("Province",
         render_kw={"placeholder": "Enter your Province"},
         validators=[DataRequired()]
    )
    postal_code = StringField("Postal Code",
         render_kw={"placeholder": "Enter your Postal Code"},
         validators=[DataRequired()]
    )
    country = StringField("Country",
         render_kw={"placeholder": "Enter your Address"},
         validators=[DataRequired()]
    )   

    submit = SubmitField("CreditCheck")

    def validate_nin(self, nin):
        existing_user = Customer().query.filter_by(sin=nin.data).first()
        if existing_user is None:
            raise ValidationError(
                "Customer does not Exist, Please provide the registered Customer infomration."
            )