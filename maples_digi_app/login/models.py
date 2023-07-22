from datetime import datetime

from flask_login import UserMixin
from maples_digi_app import db
from sqlalchemy import CheckConstraint


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    username = db.Column(db.String(255), unique=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    role_type = db.Column(
        db.String(50), CheckConstraint("role_type IN ('customer', 'employee')")
    )
    account_locked = db.Column(db.Boolean, default=False)
    last_login_date = db.Column(db.DateTime, default=datetime.now)
    created_date = db.Column(db.DateTime, default=datetime.now)
    updated_date = db.Column(
        db.DateTime, default=datetime.now, onupdate=datetime.now
    )

    # # Foreign keys
    # employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'))
    # customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))

    # # Define relationships with Employee and Customer tables
    # employee = db.relationship('Employee', backref='owner', uselist=False)
    # customer = db.relationship('Customer', backref='owner', uselist=False)

    def __repr__(self):
        return f"User{self.username}{self.email}"
