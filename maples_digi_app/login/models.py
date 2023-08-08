from datetime import datetime

from flask_login import UserMixin
from maples_digi_app import db
from sqlalchemy import BigInteger, CheckConstraint


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
    password_reset_token = db.Column(db.String(100), nullable=True)
    password_reset_token_expiration = db.Column(db.DateTime, nullable=True)
    created_date = db.Column(db.DateTime, default=datetime.now)
    updated_date = db.Column(
        db.DateTime, default=datetime.now, onupdate=datetime.now
    )

    failed_login_attempt = db.Column(db.Integer, default=0)  # New column

    def increment_failed_login(self):
        if not self.failed_login_attempt:
            self.failed_login_attempt = 1
        else:
            self.failed_login_attempt += 1

    def reset_failed_login(self):
        self.failed_login_attempt = 0
        self.account_locked = False

    # # # Foreign keys
    # # employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'))
    # # customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))

    # # # Define relationships with Employee and Customer tables
    # # employee = db.relationship('Employee', backref='owner', uselist=False)
    # # customer = db.relationship('Customer', backref='owner', uselist=False)

    # customers = db.relationship("Customer", backref="user", lazy=True)
    # employees = db.relationship("Employee", backref="user", lazy=True)

    user_association = db.relationship(
        "UserAssociation", back_populates="user", uselist=False
    )

    def __repr__(self):
        return f"User{self.username}{self.email}"
    
    def update_password(self, new_password):
        self.password = new_password
        db.session.commit()


class UserAssociation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    customer_id = db.Column(
        db.String(50), db.ForeignKey("customer.passport_no")
    )
    employee_id = db.Column(db.Integer, db.ForeignKey("employee.id"))

    # user = db.relationship(
    #     "User", backref="associations", foreign_keys=[user_id]
    # )
    # customer = db.relationship(
    #     "Customer", backref="associations", foreign_keys=[customer_id]
    # )
    # employee = db.relationship(
    #     "Employee", backref="associations", foreign_keys=[employee_id]
    # )
    user = db.relationship(
        "User", backref="associations", foreign_keys=[user_id], viewonly=True
    )
    customer = db.relationship(
        "Customer",
        backref="associations",
        foreign_keys=[customer_id],
        viewonly=True,
    )
    employee = db.relationship(
        "Employee",
        backref="associations",
        foreign_keys=[employee_id],
        viewonly=True,
    )


class Customer(db.Model, UserMixin):
    passport_no = db.Column(db.String(50), primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    first_name = db.Column(db.String(255))
    middle_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    sin = db.Column(db.Text)
    date_of_birth = db.Column(db.Date)
    address_line1 = db.Column(db.Text)
    address_line2 = db.Column(db.Text)
    city = db.Column(db.String(255))
    province = db.Column(db.String(255))
    postal_code = db.Column(db.String(20))
    country = db.Column(db.String(255))
    mobile_no = db.Column(BigInteger, nullable=False)
    nationality = db.Column(db.String(255))
    occupation = db.Column(db.String(255))
    signature = db.Column(db.LargeBinary)
    created_date = db.Column(db.DateTime, default=datetime.now)
    updated_date = db.Column(
        db.DateTime, default=datetime.now, onupdate=datetime.now
    )
    account_type = db.Column(db.String(50))

    user = db.relationship(
        "UserAssociation", back_populates="customer", uselist=False
    )

    #@property
    #def emailid(self):
        #return self.user. if self.user else None

    def __repr__(self):
        return f"Customer {self.passport_no} {self.address_line1} {self.address_line2} {self.city} {self.province} {self.postal_code} {self.country} {self.mobile_no} {self.date_of_birth} {self.sin} {self.first_name} {self.last_name}"


class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    middle_name = db.Column(db.String(255))
    date_of_birth = db.Column(db.Date)
    date_of_joining = db.Column(db.Date)
    bank_name = db.Column(db.String(255))
    instituion_no = db.Column(db.String(255))
    address_line1 = db.Column(db.Text)
    address_line2 = db.Column(db.Text)
    city = db.Column(db.String(255))
    province = db.Column(db.String(255))
    postal_code = db.Column(db.String(20))
    country = db.Column(db.String(255))
    mobile_no = db.Column(BigInteger, nullable=False)
    nationality = db.Column(db.String(255))
    designation = db.Column(db.String(255))
    auth_to_approve = db.Column(db.Boolean)
    manager_id = db.Column(db.Integer)
    signature = db.Column(db.LargeBinary)
    created_date = db.Column(db.DateTime, default=datetime.now)
    updated_date = db.Column(
        db.DateTime, default=datetime.now, onupdate=datetime.now
    )

    user = db.relationship(
        "UserAssociation", back_populates="employee", uselist=False
    )

    @property
    def emailid(self):
        return self.user.email if self.user else None

    def __repr__(self):
        return f"Employee {self.id} {self.first_name} {self.last_name} {self.date_of_birth} {self.date_of_joining} {self.designation} {self.auth_to_approve}"
