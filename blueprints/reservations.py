from flask import Blueprint, request, jsonify
from datetime import datetime
from extensions import db
from models.reservation import Reservation

reservations = Blueprint("reservations", __name__)

# ==========================
#   GET ALL RESERVATIONS
# ==========================
@reservations.get("/reservations")
def get_all():
    records = Reservation.query.all()
    return jsonify([r.to_dict() for r in records])


# ==========================
#   CHECK AVAILABILITY
# ==========================
@reservations.post("/check-availability")
def check_availability():
    data = request.json
    dt = data.get("datetime")

    if not dt:
        return jsonify({"error": "datetime is required"}), 400

    try:
        reservation_time = datetime.fromisoformat(dt)
    except ValueError:
        return jsonify({"error": "Invalid datetime format"}), 400

    exists = Reservation.query.filter_by(
        reservation_time=reservation_time
    ).first()

    return jsonify({"available": exists is None})


# ==========================
#   CREATE RESERVATION
# ==========================
@reservations.post("/reservations")
def create_reservation():
    data = request.json

    required_fields = ["customer_name", "phone", "email", "datetime", "guests"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"{field} is required"}), 400

    try:
        reservation_time = datetime.fromisoformat(data["datetime"])
    except ValueError:
        return jsonify({"error": "Invalid datetime format"}), 400

    new_reservation = Reservation(
        customer_name=data["customer_name"],
        phone=data["phone"],
        email=data["email"],
        reservation_time=reservation_time,
        guests=int(data["guests"])
    )

    db.session.add(new_reservation)
    db.session.commit()

    return jsonify(new_reservation.to_dict()), 201
