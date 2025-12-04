from datetime import datetime
from extensions import db

class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    reservation_time = db.Column(db.DateTime, nullable=False)
    guests = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "customer_name": self.customer_name,
            "phone": self.phone,
            "email": self.email,
            "reservation_time": self.reservation_time.isoformat(),
            "guests": self.guests
        }
