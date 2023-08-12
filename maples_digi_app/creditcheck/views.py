"""
Credit Check Module
This is the controller class 
    Display of Customers
    Display of Customer Details
    Credit Check Process hitting Rest API
    Display of Gauge Chart

"""
from flask import Blueprint, redirect, session, render_template, request, url_for, flash
from flask_login import current_user
from loguru import logger
from maples_digi_app.creditcheck.forms import CreditCheck_CustomerForm, CreditCheck_SubmitForm
from maples_digi_app.creditcheck.models import Cust_CreditScores
from maples_digi_app.login.models import Customer
from maples_digi_app.utils.utils import get_customer_data, get_employee_data
from maples_digi_app.utils.generate_chart import generate_gauge_chart
import requests
from datetime import datetime
import plotly.graph_objects as go
from sqlalchemy.exc import IntegrityError

creditchecks = Blueprint("creditchecks", __name__)


@creditchecks.route("/customer_details/sin", methods=["GET", "POST"])
def customer_details():
    print("Inside customer_details")
    from maples_digi_app import db
   
    logger.debug(f"Cust_CreditScores{current_user.id}")
    employee = get_employee_data()
    # logger.debug(f"Creditcheck {result} hehe")
    # customer = Customer.query.filter_by(userid=current_user.id).first()
    print("Inside customer_details",employee)

    if employee:
        # Handle case if customer doesn't exist
        logger.warning("Employee not found")
        canapprove = employee.auth_to_approve
        print("Can Approve :",canapprove)
        if canapprove == False:
            logger.error(
                f"Employee is not authorized to do a credit check {employee.first_name}. Please try again."
            )
            flash("Employee is not authorized to do a credit check. Please try again.")

    sin = request.args.get("sin")
    print("NIN :",sin)
    session['sin'] = sin
    form = CreditCheck_CustomerForm()
    customer = Customer.query.filter_by(sin=sin).first()
    
    print("Fetched Customer :",customer)
    # set customer details to the customer form
    full_name = customer.first_name + " " + customer.last_name
    form.full_name_fetch = full_name
    form.nin_fetch = str(customer.sin)
    form.date_of_birth_fetch = customer.date_of_birth
    form.address_line1_fetch = customer.address_line1
    form.address_line2_fetch = customer.address_line2
    form.city_fetch = customer.city
    form.province_fetch = customer.province
    form.postal_code_fetch = customer.postal_code
    form.country_fetch = customer.country

    return render_template(
        "customer_details.html", form=form)

@creditchecks.route("/credit_score_submit", methods=["GET", "POST"])
def credit_score_submit():

    form = CreditCheck_SubmitForm()
    logger.debug(f"Cust_CreditScores{current_user.id}")
    sin = session.get("sin")
    print("sin :",sin)

    # Replace 'http://api_url' with the actual URL of the REST API you want to hit
    api_url = f'http://localhost:5000/creditcheck/{sin}'
    message = ""
    try:
        # Make a GET request to the API with the parameter
        response = requests.get(api_url)
        print("API Response Status :", response.status_code)
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # The API response data is usually in JSON format
            data = response.json()
            print("API Response Data :", data)
            if data:
                for item in data:
                    form.credit_score.data = item['score']
                    form.credit_utilize.data = item['utilization']
                    form.credit_length.data = item['lengthInYears']
                    form.derogatory.data = item['derogatory']
                    derogatory = item['derogatory']
                    credit_score = int(item['score'])
                    cad_credit_score = ""
                    comments = ""
                    if derogatory == "No":
                        if credit_score > 700:
                            cad_credit_score = "350"
                            comments = "Very Good Credit History Back Home, Eligible for Canadaian base credit score"
                        else:
                            cad_credit_score = ""
                            comments = "Bad Credit History Back Home, Not Eligible for Canadaian base credit score"
                    
                    else:
                        cad_credit_score = ""
                        comments = "Very Bad Credit History Back Home, Having Derogatory Marks therefore Not Eligible for Canadaian base credit score"
                    form.eq_cad_score.data = cad_credit_score
                    # Get the current date and time as a datetime object
                    current_date = datetime.now()

                    form.validated_on.data = current_date
                    form.comments.data = comments
        else:
            # Handle the case where the API request was not successful
            message = "API request failed with status code :" + response.status_code
 
    except requests.RequestException as e:
        # Handle any errors that might occur during the API request
        message = e
    if message :
        flash(message)
    chart = generate_gauge_chart(credit_score)
    chart_json = chart.to_json()
    return render_template(
        "customer_creditcheck_report.html", form=form, chart_json=chart_json)

@creditchecks.route("/credit_score_save_submit", methods=["POST", "GET"])
def credit_score_save_submit():
    from maples_digi_app import db

    form = CreditCheck_SubmitForm()
    sin = session.get("sin")
    print("sin :",sin)
    message = ""
    if form.validate_on_submit():
        try:
            cust_creditscores = Cust_CreditScores(
                userid=current_user.id,
                unq_id_no=sin,
                credit_score=form.credit_score.data,
                credit_utlze=form.credit_utilize.data,
                credit_length=form.credit_length.data,
                derogatory_scr=form.derogatory.data,
                eq_cad_credit_scr=form.eq_cad_score.data,
                validated_on=form.validated_on.data,
            )
            db.session.add(cust_creditscores)
            db.session.commit()
            flash("Credit Report has been successfully saved in the portal")
            message = "Credit Report has been successfully saved in the portal"
            return render_template("/home.html", message=message)
        except IntegrityError() as err:
            logger.error(
                f"IntegrityError occurred while registering the user : {err}"
            )
            flash("Constraint violation: Please check your input.")
            message = "Constraint violation: Please check your input."
    else:
        for field, errors in form.errors.items():
            for error in errors:
                logger.error(
                    f"Validation error for field '{field}': {error}"
                )
        flash("Unable to Save the Credit Report, Please try again")
        message = "Unable to Save the Credit Report, Please try again"
        return render_template("/home.html", message=message)
