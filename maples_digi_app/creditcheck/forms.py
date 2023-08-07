from flask_wtf import FlaskForm
from wtforms import DateField, FileField, IntegerField, SelectField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError
from maples_digi_app.login.models import Customer

# from wtforms.validators import ValidationError

class CreditCheck_CustomerForm(FlaskForm):
    full_name_fetch = StringField(
       'Full Legal Name',
        validators=[DataRequired()]
    )
    
    date_of_birth_fetch = DateField(
        "Date of Birth", format="%Y-%m-%d",
        validators=[DataRequired()]
    )

    nin_fetch = StringField("National Identification Number", validators=[DataRequired()])
    
    address_line1_fetch = StringField("Address Line 1", 
        validators=[DataRequired()]
    )
    address_line2_fetch = StringField("Address Line 2",
         validators=[DataRequired()]
    )
    city_fetch = StringField("City",
         validators=[DataRequired()]
    )
    province_fetch = StringField("Province",
         validators=[DataRequired()]
    )
    postal_code_fetch = StringField("Postal Code",
         validators=[DataRequired()]
    )
    country_fetch = StringField("Country",
         validators=[DataRequired()]
    )   

    submit = SubmitField("Credit Check")

    def validate_nin(self, nin):
        existing_user = Customer().query.filter_by(sin=nin.data).first()
        if existing_user is None:
            raise ValidationError(
                "Customer does not Exist, Please provide the registered Customer infomration."
            )

class CreditCheck_SubmitForm(FlaskForm):
    credit_score = StringField(
       'Credit Score',
        validators=[DataRequired()]
    )
    
    credit_utilize = StringField(
        "Credit Utilization",
        validators=[DataRequired()]
    )

    credit_length = StringField("Credit Length in Years", 
        validators=[DataRequired()]
    )
    derogatory = StringField("Any Derogatory Marks",
         validators=[DataRequired()]
    )
    eq_cad_score = StringField("Equivalent Canadian Credit Score",
         validators=[DataRequired()]
    )
    validated_on = DateField("Validated On",
         format="%Y-%m-%d",
         validators=[DataRequired()]
    )
    comments = StringField("Credit Report Result",
         validators=[DataRequired()]
    )

    
    submit = SubmitField("Credit Report Save")

