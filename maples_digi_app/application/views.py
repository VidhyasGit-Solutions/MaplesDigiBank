from flask import Blueprint, abort, redirect, render_template, request, url_for, session
from flask_login import current_user
from loguru import logger
from maples_digi_app.application.forms import CustomerForm, EmployeeForm
from maples_digi_app.creditcheck.forms import CreditCheck_CustomerForm
from maples_digi_app.application.models import Application, StatusEnum
from maples_digi_app.login.models import Customer, Employee
from maples_digi_app.utils.utils import get_customer_data

applications = Blueprint("applications", __name__)


@applications.route("/home")
def home():
    logger.debug("Home")
    return render_template("home.html")


@applications.route("/applications", methods=["GET", "POST"])
def application():
    logger.debug(f"Applications{current_user.id}")
    customer = get_customer_data()
    # logger.debug(f"Applications {result} hehe")
    # customer = Customer.query.filter_by(userid=current_user.id).first()
    userrole = session.get('userrole')  # Access the 'userrole' session variable
    print("Session Variable - userrole :",userrole)

    if not customer:
        # Handle case if customer doesn't exist
        logger.warning("Employee found")
        return render_template(
            "applications.html", customer=None, applications=[], userrole=userrole
        )
    applications = Application.query.filter_by(
        customer_id=customer.passport_no
    ).all()

    return render_template(
        "applications.html", customer=customer, applications=applications
    )

@applications.route("/credit_score_check", methods=["GET", "POST"])
def credit_score_check():
    logger.debug(f"Credit_score_check{current_user.id}")
    form = CreditCheck_CustomerForm()

    return render_template(
        "credit_scorecheck.html", form=form)



@applications.route("/create_application", methods=["GET", "POST"])
def create_application():
    from maples_digi_app import db

    logger.debug("Create Applications")
    if current_user.role_type == "employee":
        form = EmployeeForm()
    else:
        form = CustomerForm()
    if request.method == "POST":
        logger.debug(request)
        if form.validate_on_submit():
            print(form)
            if current_user.role_type == "employee":
                # Create and add Employee object to the database
                employee = Employee(
                    employee_id=form.employee_id.data,
                    userid=current_user.id,
                    date_of_joining=form.date_of_joining.data,
                    bank_name=form.bank_name.data,
                    institution_no=form.institution_no.data,
                    designation=form.designation.data,
                    auth_to_approve=form.auth_to_approve.data,
                    manager_id=form.manager_id.data,
                )
                db.session.add(employee)
                db.session.commit()
            else:
                customer = Customer(
                    account_type=form.account_type.data,
                    passport_no=form.passport_no.data,
                    userid=current_user.id,
                    first_name=form.first_name.data,
                    middle_name=form.middle_name.data,
                    last_name=form.last_name.data,
                    sin=form.sin.data,
                    date_of_birth=form.date_of_birth.data,
                    address_line1=form.address_line1.data,
                    address_line2=form.address_line2.data,
                    city=form.city.data,
                    province=form.province.data,
                    postal_code=form.postal_code.data,
                    country=form.country.data,
                    mobile_no=form.mobile_no.data,
                    nationality=form.nationality.data,
                    occupation=form.occupation.data,
                    signature=form.signature.data,
                )
                db.session.add(customer)
                logger.debug(f"Customer {customer.passport_no} is created")
                # Create the application with the customer details
                application = Application(
                    customer_id=customer.passport_no,
                    status=StatusEnum.NEW.value,
                    application_type=customer.account_type,
                )
                db.session.add(application)
                db.session.commit()
                logger.debug(f"{application} submitted")
                return redirect(url_for("applications.home"))
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    logger.error(
                        f"Validation error for field '{field}': {error}"
                    )
    return render_template("create_application.html", form=form)


@applications.route(
    "/withdraw_application/<int:id>/<string:customer_id>",
    methods=["GET", "POST"],
)
def withdraw_application(id, customer_id):
    from maples_digi_app import db

    application = Application.query.filter_by(
        id=id, customer_id=customer_id
    ).first()

    if request.method == "POST":
        if application:
            customer = Customer.query.filter_by(passport_no=customer_id).first()
            db.session.delete(application)
            if customer:
                db.session.delete(customer)
                db.session.commit()
            logger.debug(
                f"Application {id} of customer {customer_id} is deleted"
            )
            return redirect("/home")
        else:
            abort(404)

    return render_template(
        "delete_application.html", application_type=application.application_type
    )
