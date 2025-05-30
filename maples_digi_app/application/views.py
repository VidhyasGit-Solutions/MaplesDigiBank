from flask import Blueprint,Response,flash, abort, redirect, render_template, request, url_for, session
from flask_login import current_user
from loguru import logger
from datetime import datetime, timedelta
from maples_digi_app.application.forms import CustomerForm, EmployeeForm
from maples_digi_app.creditcheck.forms import CreditCheck_CustomerForm
from maples_digi_app.application.models import Application, StatusEnum
from maples_digi_app.login.models import Customer, Employee, UserAssociation
from maples_digi_app.utils.utils import allowed_file, get_customer_data, get_employee_data
from sqlalchemy import or_
from werkzeug.utils import secure_filename


applications = Blueprint("applications", __name__)

# route handler for the URL path "/home".
@applications.route("/home")
def home():
    logger.debug("Home")
    return render_template("home.html")


@applications.route("/applications", methods=["GET", "POST"])
# display of applications based on the user's role (customer or employee)
def application():
    logger.debug(f"Applications{current_user.id}")
    customer = get_customer_data()
    employee = get_employee_data()
    # logger.debug(f"Applications {result} hehe")
    # customer = Customer.query.filter_by(userid=current_user.id).first()
    userrole = session.get('userrole')  # Access the 'userrole' session variable
    print("Session Variable - userrole :",userrole)

    if current_user.role_type == "employee" and not employee:
        form = EmployeeForm()
        return render_template(
            "create_employee_application.html", form=form, employee=True
        )
    
    applications = []
    if customer:
        applications = Application.query.filter_by(
            customer_id=customer.passport_no
        ).all()

    elif employee:
        applications = Application.query.filter(
            or_(
                Application.employee_id == employee.id,
                Application.employee_id.is_(None),
            )
        ).all()
    
    # if not customer:
    #     # Handle case if customer doesn't exist
    #     logger.warning("Employee found")
    #     return render_template(
    #         "applications.html", customer=None, applications=[], userrole=userrole
    #     )
    return render_template(
        "applications.html",
        customer=customer,
        applications=applications,
        employee=employee,
    )
   

@applications.route("/customer_list", methods=["GET", "POST"])
def customer_list():
    logger.debug(f"Customer{current_user.id}")
    from maples_digi_app import db
    # Retrieve list of customer ids associated with the current user
    print("Current User ID :", current_user.id)
    customer_ids  = UserAssociation.query.with_entities(UserAssociation.customer_id).filter_by(user_id=current_user.id).all()
    print("Fetched customer_ids :", customer_ids)
    # Retrieve customer IDs associated with the current employee (user)
    print("Fetched customer_ids :", customer_ids)
    
    # Fetch customers associated with the list of customer IDs
    # Convert the list of tuples to a list of customer IDs
    customer_ids = [customer_id[0] for customer_id in customer_ids]

    # Now you can use the list of customer IDs for further processing, e.g., fetching customers
    customers = Customer.query.filter(Customer.passport_no.in_(customer_ids)).all()

    return render_template("customer_list.html", customers=customers)



@applications.route("/create_application", methods=["GET", "POST"])
def create_application():
    from maples_digi_app import db
    # Logging debug message for tracking
    logger.debug("Create Applications")
    if current_user.role_type == "employee":
        form = EmployeeForm()
    else:
        form = CustomerForm()
    if request.method == "POST":
        logger.debug(request)
        if form.validate_on_submit():
            print(form)
             # Determine the form to use based on the user's role
            if current_user.role_type == "employee":
                # Create and add Employee object to the database
                employee = Employee(
                    userid=current_user.id,
                    date_of_joining=form.date_of_joining.data,
                    bank_name="Maple Digi Bank",
                    designation=form.designation.data,
                    auth_to_approve=False,
                    manager_id=form.manager_id.data,
                    first_name=form.first_name.data,
                    middle_name=form.middle_name.data,
                    last_name=form.last_name.data,
                    date_of_birth=form.date_of_birth.data,
                    address_line1=form.address_line1.data,
                    address_line2=form.address_line2.data,
                    city=form.city.data,
                    province=form.province.data,
                    postal_code=form.postal_code.data,
                    country=form.country.data,
                    mobile_no=form.mobile_no.data,
                    nationality=form.nationality.data,
                    signature=form.signature.data.encode("utf-8"),
                )
                db.session.add(employee)
                db.session.commit()
                return redirect(url_for("applications.home"))
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
                    signature=form.signature.data.encode("utf-8"),
                )
                db.session.add(customer)
                logger.debug(f"Customer {customer.passport_no} is created")
                # Create the application with the customer details
                filename = None
                file_content = None
                if form.passport_file.data:  # Check if a file was uploaded
                    file = form.passport_file.data
                    filename = secure_filename(file.filename)
                    file_content = file.read()
                application = Application(
                    customer_id=customer.passport_no,
                    status=StatusEnum.NEW.value,
                    application_type=customer.account_type,
                    submitted_on=form.submitted_on.data,
                    passport_file=file_content,
                    passport_file_name=filename,
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
                    flash(error)
    if current_user.role_type == "employee":
        return render_template(
            "create_employee_application.html", form=form, employee=True
        )
    else:
        return render_template("create_application.html", form=form)

# Define a route handler for "/edit_application" URL path with customer_id parameter
@applications.route(
    "/edit_application/<string:customer_id>", methods=["GET", "POST"]
)
def edit_application(customer_id):
    from maples_digi_app import db

    logger.debug("Edit Applications")
    if current_user.role_type == "employee":
        return "Not Supported"
    else:
        form = CustomerForm()
    # Logic to handle application editing based on status
    # Redirect user to home route after successful update
    # Log validation errors if the form is not valid
    customer = Customer.query.get_or_404(customer_id)
    logger.debug(f"Customer {customer} is found")
    customer = Customer.query.filter_by(
        passport_no=customer_id, userid=current_user.id
    ).first()
    application = Application.query.filter_by(customer_id=customer_id).first()
    logger.debug(
        f"Customer {customer_id} Application {application.id} is in {application.status.value} state"
    )
    if application.status != StatusEnum.NEW:
        logger.debug(
            f"Application {application.id} is in {application.status.value} state"
        )
        return "Application is in progress. Edit is disabled"
    if request.method == "POST":
        logger.debug(request)
        logger.info(f"signature {form.signature.data}")
        if form.validate_on_submit():
            # Logic for handling form submission based on user's role
            # If user is an employee, create and add Employee object to the database
            # If user is a customer, create Customer and Application objects
            
            passport_no = form.passport_no.data
            update_data = {
                Customer.first_name: form.first_name.data,
                Customer.middle_name: form.middle_name.data,
                Customer.last_name: form.last_name.data,
                Customer.sin: form.sin.data,
                Customer.date_of_birth: form.date_of_birth.data,
                Customer.address_line1: form.address_line1.data,
                Customer.address_line2: form.address_line2.data,
                Customer.city: form.city.data,
                Customer.province: form.province.data,
                Customer.postal_code: form.postal_code.data,
                Customer.country: form.country.data,
                Customer.mobile_no: form.mobile_no.data,
                Customer.nationality: form.nationality.data,
                Customer.occupation: form.occupation.data,
                Customer.updated_date: datetime.now(),
                Customer.account_type: form.account_type.data,
            }
            if form.signature.data:
                # Check if a signature has been provided in the form
                logger.info("signature updated")
                update_data[Customer.signature] = form.signature.data.encode(
                    "utf-8"
                )
            else:
                logger.info("signature not updated")
            # Perform the update query
            db.session.query(Customer).filter_by(
                passport_no=passport_no
            ).update(update_data)

            update_application = {
                Application.updated_date: datetime.now(),
                Application.submitted_on: form.submitted_on.data,
            }

            if form.passport_file.data:
                # Check if a passport file has been uploaded in the form
                file = form.passport_file.data
                filename = secure_filename(file.filename)
                file_content = file.read()
                # Update the application's passport file and passport file name with the new content and filename
                update_application[Application.passport_file] = file_content
                update_application[Application.passport_file_name] = filename
            db.session.query(Application).filter_by(
                customer_id=customer_id
            ).update(update_application)

            db.session.commit()

            return redirect(url_for("applications.home"))
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    logger.error(
                        f"Validation error for field '{field}': {error}"
                    )

    elif request.method == "GET":
        logger.debug(f"Application submitted on {application.submitted_on}")
        logger.debug(
            f"Application submitted on {type(application.submitted_on)}"
        )
        form.account_type.data = customer.account_type
        form.passport_no.data = customer.passport_no
        form.first_name.data = customer.first_name
        form.middle_name.data = customer.middle_name
        form.last_name.data = customer.last_name
        form.sin.data = customer.sin
        form.date_of_birth.data = customer.date_of_birth
        form.address_line1.data = customer.address_line1
        form.address_line2.data = customer.address_line2
        form.city.data = customer.city
        form.province.data = customer.province
        form.postal_code.data = customer.postal_code
        form.country.data = customer.country
        form.mobile_no.data = customer.mobile_no
        form.nationality.data = customer.nationality
        form.occupation.data = customer.occupation
        form.signature.data = customer.signature.decode("utf-8")
        form.submitted_on.data = application.submitted_on
        form.passport_file = application.passport_file
        form.passport_file_name = application.passport_file_name
        form.application_id = application.id
        return render_template("edit_application.html", form=form)

    else:
        return "Not Supported"


# Define a route handler for "/view_file" URL path with application_id parameter
@applications.route("/view_file/<int:application_id>")
def view_file(application_id):
    application = Application.query.get_or_404(application_id)
    logger.debug(
        f"current_user.id {current_user.id}, application {application}, {application.customer.userid}"
    )
    # Check if the current user has permission to view the file
    if current_user.id == application.customer.userid:
        if application.passport_file and allowed_file(
            application.passport_file_name
        ):
            content_type = (
                "application/pdf"
                if application.passport_file_name.endswith(".pdf")
                else "image/jpeg"
                if application.passport_file_name.endswith((".jpg", ".jpeg"))
                else "image/png"
            )
            response = Response(
                application.passport_file, content_type=content_type
            )
            response.headers[
                "Content-Disposition"
            ] = f"inline; filename={application.passport_file_name}"
            response.headers["Content-Length"] = len(
                application.passport_file
            )  # Set content length
            return response
        return "File not found."
    else:
        return "Unauthorized or File not found."


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
