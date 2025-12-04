import random
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
        reservation_date = datetime.fromisoformat(dt)
    except ValueError:
        return jsonify({"error": "Invalid datetime format"}), 400

    exists = Reservation.query.filter_by(
        reservation_date=reservation_date
    ).first()

    return jsonify({"available": exists is None})


# ==========================
#   CREATE RESERVATION
# ==========================
@reservations.post("/reservations")
def create_reservation():
    data = request.json

    required_fields = [
        "customer_name",
        "phone",
        "email",
        "reservation_date",
        "start_time",
        "end_time",
        "guests"
    ]

    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"{field} is required"}), 400

    # ----------- 1. Validate date/time ahead -----------
    try:
        reservation_date = datetime.strptime(data["reservation_date"], "%Y-%m-%d").date()
        start_time = datetime.strptime(data["start_time"], "%H:%M").time()
        end_time = datetime.strptime(data["end_time"], "%H:%M").time()
    except ValueError:
        return jsonify({"error": "Invalid date or time format"}), 400

    now = datetime.now()
    reservation_datetime = datetime.combine(reservation_date, start_time)

    if reservation_datetime <= now:
        return jsonify({"error": "Reservation date/time must be ahead"}), 400

    if end_time <= start_time:
        return jsonify({"error": "End time must be after start time"}), 400

    # ----------- 2. Check Overlapping Slot BEFORE assigning table -----------

    overlap = Reservation.query.filter(
        Reservation.reservation_date == reservation_date,
        Reservation.start_time < end_time,
        Reservation.end_time > start_time
    ).all()

    # If 30 tables are fully taken = no availability
    if len(overlap) >= 30:
        return jsonify({"error": "Time slot is fully booked"}), 400

    # ----------- 3. Assign a Random Table 1–30 ----------
    # get tables already taken for this time window
    taken_tables = [r.table_number for r in overlap]

    free_tables = [t for t in range(1, 31) if t not in taken_tables]

    if not free_tables:
        return jsonify({"error": "No free table available for this time slot"}), 400

    assigned_table = random.choice(free_tables)

    # ----------- 4. Create Reservation -----------
    new_reservation = Reservation(
        customer_name=data["customer_name"],
        phone=data["phone"],
        email=data["email"],
        reservation_date=reservation_date,
        start_time=start_time,
        end_time=end_time,
        guests=data["guests"],
        table_number=assigned_table,
    )

    db.session.add(new_reservation)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Reservation successful",
        "table_number": assigned_table
    }), 201


