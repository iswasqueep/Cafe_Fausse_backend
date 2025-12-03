from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

# Initialize app
app = Flask(__name__)
CORS(app)

# Database config
app.config['SQLALCHEMY_DATABASE_URI'] = (
    "postgresql+psycopg2://postgres:admin@localhost/cafe_fausse_db"
)

db = SQLAlchemy(app)


# ===========================
#       DATABASE MODEL
# ===========================
class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(100))
    phone = db.Column(db.String(100))
    email = db.Column(db.String(100))
    datetime = db.Column(db.String(100))  # ideally this should be DateTime type
    guests = db.Column(db.String(100))

    def to_dict(self):
        return {
            "id": self.id,
            "customer_name": self.customer_name,
            "phone": self.phone,
            "email": self.email,
            "datetime": self.datetime,
            "guests": self.guests
        }


# ===========================
#          ROUTES
# ===========================

@app.route("/reservations", methods=["GET"])
def get_users():
    users = Reservation.query.all()
    return jsonify([u.to_dict() for u in users])


@app.route("/check-availability", methods=["POST"])
def checkavailability():
    data = request.json
    reservation_dt = data.get("datetime")

    try:
        reservation_date = datetime.fromisoformat(reservation_dt)
    except:
        return jsonify({"error": "Invalid date format"}), 400

    # Check if date already booked
    existing = Reservation.query.filter_by(datetime=reservation_dt).first()
    if existing:
        return jsonify({"error": "Date already booked"}), 200

    return jsonify({"available": True}), 200


@app.route("/createuser", methods=["POST"])
def create_user():
    data = request.json
    
    user = Reservation(
        customer_name=data["customer_name"],
        phone=data["phone"],
        email=data["email"],
        datetime=data["datetime"],
        guests=data["guests"]
    )

    db.session.add(user)
    db.session.commit()

    return jsonify(user.to_dict()), 201


# ===========================
#         APP RUNNER
# ===========================
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
