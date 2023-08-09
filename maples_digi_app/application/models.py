from datetime import datetime

from flask_login import UserMixin
from maples_digi_app import db
from maples_digi_app.utils.constants import StatusEnum


class Application(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(
        db.String(50), db.ForeignKey("customer.passport_no"), nullable=False
    )
    employee_id = db.Column(db.Integer, db.ForeignKey("employee.id"))

    status = db.Column(
        db.Enum(StatusEnum, name="status_enum"),
        default=StatusEnum.NEW,
        server_default="NEW",
    )
    application_type = db.Column(db.String(50))
    passport_file = db.Column(db.LargeBinary)
    passport_file_name = db.Column(db.String(255))

    customer = db.relationship("Customer", backref="application", lazy=True)
    employee = db.relationship("Employee", backref="applications", lazy=True)
    submitted_on = db.Column(db.DateTime)

    created_date = db.Column(db.DateTime, default=datetime.now)
    updated_date = db.Column(
        db.DateTime, default=datetime.now, onupdate=datetime.now
    )

    def __repr__(self):
        return f"Application {self.id} for Customer {self.customer_id}"

    @property
    def status_percentage(self):
        progress = None
        color = "blue"
        text_color = "blue"
        if self.status == StatusEnum.NEW:
            progress = 25
            text_color = "yellow"
        elif self.status == StatusEnum.IN_PROGRESS:
            progress = 50
            color = "yellow"
        elif self.status == StatusEnum.UNDER_REVIEW:
            progress = 80
            color = "orange"
        elif self.status == StatusEnum.COMPLETED:
            progress = 100
            color= "green"
        elif self.status == StatusEnum.REJECTED:
            progress = 100
            color = "red"
        else:
            progress = 0
            color = "green"
        print(f"********progress {progress}")
        return [progress, color, text_color]
