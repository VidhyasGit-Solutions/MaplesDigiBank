from datetime import datetime

from flask_login import UserMixin
from maples_digi_app import db

class Cust_CreditScores(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userid = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    unq_id_no = db.Column(db.String(150))
    credit_score = db.Column(db.String(150))
    credit_utlze = db.Column(db.String(150))
    credit_length = db.Column(db.String(150))
    derogatory_scr = db.Column(db.String(150))
    eq_cad_credit_scr = db.Column(db.String(150))
    validated_on = db.Column(db.Date)
    created_date = db.Column(db.DateTime, default=datetime.now)
    updated_date = db.Column(
        db.DateTime, default=datetime.now, onupdate=datetime.now
    )

    def __repr__(self):
        return f"Cust_CreditScores {self.cust_crsc_id} {self.userid} {self.unq_id_no} {self.credit_score} {self.credit_utlze} {self.credit_length} {self.derogatory_scr} {self.eq_cad_credit_scr} {self.validated_on}"
