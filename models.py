from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()




class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(100))
    phone = db.Column(db.String(100))
    email = db.Column(db.String(100))
    datetime = db.Column(db.String(100))
    guests = db.Column(db.String(100))

    def to_dict(self):
        return {"id": self.id, "customer_name": self.customer_name, "phone": self.phone, "email": self.email, "datetime": self.datetime, "guests": self.guests}


# class Reservation(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     customer_name = db.Column(db.String(100))
#     phone = db.Column(db.String(100))
#     email = db.Column(db.String(100))
#     datetime = db.Column(db.String(100))
#     guests = db.Column(db.String(100))
#     seat_number = db.Column(db.Integer)  # UPDATED NAME

#     def to_dict(self):
#         return {
#             "id": self.id,
#             "customer_name": self.customer_name,
#             "phone": self.phone,
#             "email": self.email,
#             "datetime": self.datetime,
#             "guests": self.guests,
#             "seat_number": self.seat_number
#         }