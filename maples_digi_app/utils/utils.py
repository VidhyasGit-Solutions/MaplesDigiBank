from flask_login import current_user
from loguru import logger
from maples_digi_app.login.models import Customer, Employee
import requests


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

def get_manager_data():
    if current_user.is_authenticated:
        manager = Employee.query.filter_by(designation="manager").all()
        if manager:
            return manager
        else:
            logger.warning("manager data not found.")
            return None
    else:
        # Handle case if user is not authenticated
        logger.error(f"{current_user} User not authenticated")
        return None


def send_email(recipient, body, subject):
    api_key = "api-D748F98C362911EE8888F23C91C88F4E"
    api_url = "https://api.smtp2go.com/v3/email/send"

    sender = "shireesha289@gmail.com"
    html_body = f"<h1>{subject}</h1><br>{body}"

    payload = {
        "api_key": api_key,
        "to": [recipient],
        "sender": sender,
        "subject": subject,
        "text_body": body,
        "html_body": html_body,
    }
    headers = {"Content-Type": "application/json"}

    response = requests.post(api_url, json=payload, headers=headers)
    logger.info(response.text)
    if response.status_code == 200:
        return "Email sent successfully!"
    else:
        return "Failed to send email"