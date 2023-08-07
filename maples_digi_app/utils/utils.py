from flask_login import current_user
from loguru import logger
from maples_digi_app.login.models import Customer, Employee


def get_customer_data():
    if current_user.is_authenticated:
        customer = Customer.query.filter_by(userid=current_user.id).first()
        if customer:
            return customer
        else:
            logger.warning("Customer data not found.")
            return None
    else:
        # Handle case if user is not authenticated
        logger.error(f"{current_user} User not authenticated")
        return None

def get_employee_data():
    if current_user.is_authenticated:
        employee = Employee.query.filter_by(userid=current_user.id).first()
        print("Inside get_employee_data", employee)
        if employee:
            return employee
        else:
            logger.warning("employee data not found.")
            return None
    else:
        # Handle case if user is not authenticated
        logger.error(f"{current_user} Employee not authenticated")
        return None
