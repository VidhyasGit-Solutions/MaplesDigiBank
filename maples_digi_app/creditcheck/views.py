from flask import Blueprint, abort, redirect, render_template, request, url_for, flash
from flask_login import current_user
from loguru import logger
from maples_digi_app.creditcheck.forms import CreditCheck_CustomerForm
from maples_digi_app.creditcheck.models import Cust_CreditScores
from maples_digi_app.utils.utils import get_customer_data, get_employee_data

creditchecks = Blueprint("creditchecks", __name__)


@creditchecks.route("/credit_score_submit", methods=["GET", "POST"])
def credit_score_submit():

    form = CreditCheck_CustomerForm()
    logger.debug(f"Cust_CreditScores{current_user.id}")
    employee = get_employee_data()
    # logger.debug(f"Creditcheck {result} hehe")
    # customer = Customer.query.filter_by(userid=current_user.id).first()

    if not employee:
        # Handle case if customer doesn't exist
        logger.warning("Employee not found")
        canapprove = employee.auth_to_approve
        if canapprove == 1:
            logger.error(
                f"Employee is not authorized to do a credit check {employee.first_name}. Please try again."
            )
            flash("Employee is not authorized to do a credit check. Please try again.")
    return render_template(
        "credit_scorecheck.html", form=form)