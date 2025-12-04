from datetime import datetime
from extensions import db

class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    reservation_date = db.Column(db.DateTime, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    guests = db.Column(db.Integer, nullable=False)
    table_number = db.Column(db.String(5))


    def to_dict(self):
        return {
            "id": self.id,
            "customer_name": self.customer_name,
            "phone": self.phone,
            "email": self.email,
            "reservation_date": self.reservation_date.strftime("%Y-%m-%d %H:%M:%S") 
                            if hasattr(self.reservation_date, "strftime") else self.reservation_date,
            "start_time": self.start_time.strftime("%H:%M:%S") 
                      if hasattr(self.start_time, "strftime") else self.start_time,
            "end_time": self.end_time.strftime("%H:%M:%S") 
                    if hasattr(self.end_time, "strftime") else self.end_time,
            "guests": self.guests,
            "table_number": self.table_number
        }
