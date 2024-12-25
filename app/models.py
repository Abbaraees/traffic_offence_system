from datetime import datetime

from app import db, login_manager

# User Loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='marshal')  # Roles: admin, marshal
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<User {self.username}>"

# Offence Model
class Offence(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10), unique=True, nullable=False)
    description = db.Column(db.String(255), nullable=False)
    penalty = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Offence {self.code}>"

# Offender Model
class Offender(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    license_number = db.Column(db.String(20), unique=True, nullable=False)
    plate_number = db.Column(db.String(20), unique=True, nullable=False)
    contact_info = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Offender {self.name}>"

# Offender-Offence Relationship Model
class OffenderOffence(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    offender_id = db.Column(db.Integer, db.ForeignKey('offender.id'), nullable=False)
    offence_id = db.Column(db.Integer, db.ForeignKey('offence.id'), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='unpaid')  # unpaid, paid, appealed
    date_committed = db.Column(db.DateTime, default=datetime.utcnow)

    offender = db.relationship('Offender', backref=db.backref('offences', lazy=True))
    offence = db.relationship('Offence', backref=db.backref('offenders', lazy=True))

    def __repr__(self):
        return f"<OffenderOffence {self.offender_id}-{self.offence_id}>"

# Payment Model
class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    offender_id = db.Column(db.Integer, db.ForeignKey('offender.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='unpaid')  # unpaid, paid
    payment_date = db.Column(db.DateTime, nullable=True)

    offender = db.relationship('Offender', backref=db.backref('payments', lazy=True))

    def __repr__(self):
        return f"<Payment {self.offender_id} - {self.amount}>"

