from flask import Flask, request, jsonify, render_template, send_file, flash, url_for, redirect, session
import kagglehub
from kagglehub import KaggleDatasetAdapter
import pandas as pd
import joblib
import numpy as np
from pymongo import MongoClient, DESCENDING
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import gridfs
import certifi
from bson.objectid import ObjectId
from bson.json_util import dumps
import json
import io
from flask_socketio import SocketIO, emit
from collections import defaultdict
from datetime import datetime, time, timezone, timedelta
from flask_cors import CORS
import certifi
import pytz



# Flask App Configuration
app = Flask(__name__)
socketio = SocketIO(app)
app.secret_key = 'thiskeyissupposedtobeprivateandonlyknowbytheadmin'
CORS(app)

# Use a single connection for both PyMongo and GridFS
MONGO_URI = "mongodb+srv://udofiaubong10:qAWzNlJT6x2vSCdb@dsamessenger.tqp9u.mongodb.net/e_ticketing"
mongo_client = MongoClient(MONGO_URI, tlsCAFile=certifi.where())  # Secure TLS connection

# Set up database and GridFS
db = mongo_client["e_ticketing"]
users_collection = db["users"]
admin_collection = db["admin"]
routes_collection = db["routes"]  # Collection storing routes
stations_collection = db["stations"]  # Collection storing stations
train_schedules_collection = db["train_schedules"]  # Collection storing train schedules
bookings_collection = db["bookings"]
fs = gridfs.GridFS(db)  # GridFS instance



# Load trained models
train_delay_model = joblib.load("train_delay_model.pkl")
seat_model = joblib.load("seat_availability_model.pkl")
peak_model = joblib.load("peak_hour_model.pkl")



# Allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def index():
    return render_template("index.html")



@app.route("/login")
def login():
    return render_template("login.html")



@app.route("/register")
def register():


    return render_template("register.html")


@app.route("/user_dashboard")
def user_dashboard():


    return render_template("user_dashboard.html")



def convert_objectid(doc):
    """Recursively converts ObjectId fields in a document to strings."""
    if isinstance(doc, list):
        return [convert_objectid(d) for d in doc]
    elif isinstance(doc, dict):
        return {k: str(v) if isinstance(v, ObjectId) else convert_objectid(v) for k, v in doc.items()}
    return doc

@app.route("/destination")
def destination():
    # Fetch all routes (excluding _id to avoid serialization issues)
    routes = list(routes_collection.find({}, {"_id": 0, "route_name": 1, "stations": 1}))

    # Fetch seat availability and convert all ObjectIds to strings
    seat_availability = list(train_schedules_collection.find({}, {"train_id": 1, "train_name": 1, "route_id": 1, "available_seats": 1, "seats": 1}))
    seat_availability = convert_objectid(seat_availability)  # Convert ObjectId recursively

    # Extract unique station names
    stations = list({station["station_name"] for route in routes for station in route.get("stations", [])})

    return render_template("destination.html", routes=routes, stations=stations, seat_availability=seat_availability)



@app.route("/booking_confirmation")
def book_confirmation():
    # fetch booking details to the booking confirmation page

    bookings = list(bookings_collection.find({}, {"_id": 0, "passenger_name": 1, "phone_number": 1, "route_name": 1, "train_name": 1, "departure": 1, "arrival": 1, "seat_number": 1, "price": 1, "departure_time": 1, "booking_date": 1}))



    return render_template("booking_confirmation.html", bookings=bookings)



@app.route("/success")
def success():
    # fetch booking details to the booking confirmation page

    bookings = list(bookings_collection.find({}, {"_id": 1, "passenger_name": 1, "phone_number": 1, "route_name": 1, "train_name": 1, "departure": 1, "arrival": 1, "seat_number": 1, "price": 1, "departure_time": 1, "booking_date": 1}))



    return render_template("success.html", bookings=bookings)

# ----------------------------------------------------------------------------------------
@app.route("/profile_picture/<user_id>")
def get_profile_picture(user_id):
    try:
        user = users_collection.find_one({"_id": ObjectId(user_id)})
        if user and "profile_picture" in user:
            file_id = user["profile_picture"]
            file_data = fs.get(ObjectId(file_id))  # Ensure file_id is an ObjectId
            return send_file(io.BytesIO(file_data.read()), mimetype="image/jpeg")
        return "No Image", 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
# ------------------------------------------------------------------------------------------


@app.route("/submit_register", methods=["POST"])
def submit_register():
    try:
        # Fetch data from the form
        firstname = request.form.get("firstname")
        lastname = request.form.get("lastname")
        email = request.form.get("email")
        phone = request.form.get("phone")
        password = request.form.get("password_hash")
        con_password = request.form.get("con_password_hash")
        role = request.form.get("role")
        status = request.form.get("status")
        profile_picture = request.files.get("profile_picture")

        print(f"Received data: {firstname}, {lastname}, {email}, {phone}")

        # Validation check
        if password != con_password:
            return jsonify({"success": False, "error": "Passwords do not match!"}), 400

        if users_collection.find_one({"email": email}):
            return jsonify({"success": False, "error": "Email is already registered!"}), 400

        hashed_password = generate_password_hash(password)

        # File handling with GridFS
        file_id = None
        if profile_picture:
            filename = secure_filename(profile_picture.filename)
            file_id = fs.put(profile_picture, filename=filename)
            print(f"Profile picture uploaded, file ID: {file_id}")
        else:
            print("No profile picture uploaded")

        # Prepare user data
        user_data = {
            "firstname": firstname,
            "lastname": lastname,
            "email": email,
            "phone": phone,
            "password": hashed_password,
            "role": role,
            "status": status,
            "profile_picture": file_id,
            "timezone": datetime.now(timezone.utc).isoformat()
        }

        # Insert user data into MongoDB
        users_collection.insert_one(user_data)
        print("User registered successfully")

        # Emit event (to notify frontend)
        socketio.emit('user_registered', {'username': firstname + " " + lastname, 'email': email}, room=None)
        print("Event emitted for new user registration")

        return jsonify({"success": True, "message": "Registration successful! You can now log in."}), 200

    except Exception as e:
        print(f"Error occurred: {str(e)}")  # Log the actual error
        return jsonify({"success": False, "error": "An error occurred while registering the user."}), 500

# -----------------------------------------------------------------------

# User login route
@app.route("/submit_login", methods=["POST"])
def submit_login():
    email = request.json.get("email")  # Use request.json since you're sending JSON data
    password = request.json.get("password")

    user = users_collection.find_one({"email": email})

    if user and check_password_hash(user["password"], password):
        session["user"] = user["email"]  # Store email in session
        session["role"] = user["role"]  # Store user role

        # Return a JSON response with success status and redirect URL
        return jsonify({
            "success": True,
            "redirect": url_for("user_dashboard")
        })
    else:
        return jsonify({
            "success": False,
            "error": "Invalid email or password!"
        }), 400
   
# -------------------------------------------------------------------
@socketio.on('user_registered')
def handle_user_registration(data):
    # Emit event to frontend to update the chart
    socketio.emit('user_registered', {'username': data['username'], 'email': data['email']}, broadcast=True)

# Other event
@socketio.on('payment_ticket_update')
def handle_payment_ticket(data):
    socketio.emit('payment_ticket_update', {'ticket_info': data}, broadcast=True)


# ------------------------------------------------------------------
# User login route
@app.route("/admin_login", methods=["POST"])
def admin_login():
    email = request.json.get("email")  # Use request.json since you're sending JSON data
    password = request.json.get("password")

    admin = admin_collection.find_one({"email": email})

    if admin and check_password_hash(admin["password"], password):
        session["user"] = admin["email"]  # Store email in session
        session["role"] = admin["role"]  # Store user role

        # Return a JSON response with success status and redirect URL
        return jsonify({
            "success": True,
            "redirect": url_for("dashboard")
        })
    else:
        return jsonify({
            "success": False,
            "error": "Invalid email or password!"
        }), 400
   


# -------------------------------------------------------------------

@app.route("/admin")
def admin():
    if "user" not in session:
        return redirect(url_for("login"))

    user = {"email": session.get("user")}
    return render_template("admin.html", user=user, content="admin.html")
 
@app.route('/dashboard')
def dashboard():
    return render_template("admin.html", content="partials/dashboard.html")

@app.route('/users')
def users():
    return render_template("admin.html", content="partials/users.html")

@app.route('/tickets')
def tickets():
    return render_template("admin.html", content="partials/tickets.html")

@app.route('/trains')
def trains():
    return render_template("admin.html", content="partials/trains.html")

@app.route('/train_routes')
def stations():
    return render_template("admin.html", content="partials/train_routes.html")

@app.route('/payments')
def payments():
    return render_template("admin.html", content="partials/payments.html")

@app.route('/analytics')
def analytics():
    return render_template("admin.html", content="partials/analytics.html")

@app.route('/settings')
def settings():
    return render_template("admin.html", content="partials/settings.html")

# -------------------------------------------------------------------------------------


@app.route("/dashboard_stats", methods=["GET"])
def get_dashboard_stats():
    try:
        total_users = users_collection.count_documents({})
        total_trains = trains_collection.count_documents({})

        return jsonify({
            "total_users": total_users,
            "total_trains": total_trains
        }), 200
    except Exception as e:
        print("Error fetching dashboard stats:", str(e))
        return jsonify({"error": str(e)}), 500


# ------------------------------------------------------------------------------------
# User logout route
@app.route("/logout")
def logout():
    session.pop("user", None)  # Remove user from session
    session.pop("role", None)
    flash("You have been logged out.", "info")
    return redirect(url_for("login"))



# TRAINED MODEL:

# 🚆 1. Predict Train Delay
# @app.route("/predict_delay", methods=["POST"])
# def predict_delay():
#     data = request.get_json()
#     df = pd.DataFrame([data])  # Convert to DataFrame
    
#     # Convert categorical variables
#     df = pd.get_dummies(df, columns=["Source Station", "Destination Station"])
    
#     prediction = train_delay_model.predict(df)
#     return jsonify({"delayed": bool(prediction[0])})

# # 🎟 2. Predict Seat Availability
# @app.route("/predict_seats", methods=["POST"])
# def predict_seats():
#     data = request.get_json()
#     df = pd.DataFrame([data])  # Convert to DataFrame
    
#     # Convert categorical variables
#     df = pd.get_dummies(df, columns=["Source Station", "Destination Station"])
    
#     prediction = seat_model.predict(df)
#     return jsonify({"available_seats": int(prediction[0])})

# # ⏳ 3. Predict Peak Hours
# @app.route("/predict_peak", methods=["GET"])
# def predict_peak():
#     hours = pd.DataFrame({"Arrival Hour": list(range(24))})
#     future_trains = peak_model.predict(hours)
    
#     peak_hours = {int(h): int(t) for h, t in zip(hours["Arrival Hour"], future_trains)}
#     return jsonify(peak_hours)



@app.route("/predict_delay", methods=["POST"])
def predict_delay():
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "Invalid or missing JSON data"}), 400

    df = pd.DataFrame([data])  # Convert to DataFrame
    
    # Ensure categorical variables exist
    if "Source Station" not in df.columns or "Destination Station" not in df.columns:
        return jsonify({"error": "Missing required fields"}), 400

    df = pd.get_dummies(df, columns=["Source Station", "Destination Station"])
    
    # Mocking model prediction for testing (replace with actual model)
    prediction = [0]  # train_delay_model.predict(df)
    return jsonify({"delayed": bool(prediction[0])})

@app.route("/predict_seats", methods=["POST"])
def predict_seats():
    data = request.get_json()
    df = pd.DataFrame([data])  

    # Handle categorical variables
    df = pd.get_dummies(df, columns=["Source Station", "Destination Station"])
    
    prediction = seat_model.predict(df)

    # Return an array for better chart visualization
    return jsonify({"available_seats": list(map(int, prediction))})


@app.route("/predict_peak", methods=["GET"])
def predict_peak():
    hours = pd.DataFrame({"Arrival Hour": list(range(24))})
    
    # Mocking model prediction for testing (replace with actual model)
    future_trains = [5] * 24  # peak_model.predict(hours)
    
    peak_hours = {int(h): int(t) for h, t in zip(hours["Arrival Hour"], future_trains)}
    return jsonify(peak_hours)
# 


# ------------------------------------- USERS COLLECTIONS STARTS HERE ----------------------------------------------

users_collection = db["users"]

# Helper function to convert MongoDB documents
def serialize_user(user):
    user["_id"] = str(user["_id"])  # Convert _id to string
    if "profile_picture" in user and isinstance(user["profile_picture"], ObjectId):
        user["profile_picture"] = str(user["profile_picture"])  # Convert profile_picture ID
    return user

@app.route('/get_users', methods=['GET'])
def get_users():
    try:
        users = list(users_collection.find())  # Fetch all users
        users = [serialize_user(user) for user in users]  # Convert ObjectId
        return jsonify(users), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ----------------------------- REGISTRATION VISUALIZATION -----------------------------------

@app.route("/user_registration_trend", methods=["GET"])
def user_registration_trend():
    try:
        # Fetch user registration timestamps
        users = list(users_collection.find({}, {"_id": 0, "timestamp": 1}).sort("timestamp", DESCENDING))

        # Check if users exist
        if not users:
            return jsonify({"error": "No users found"}), 404

        # Convert timestamps to human-readable dates
        registration_data = []
        for user in users:                                                                          
            if "timestamp" in user:
                try:
                    timestamp = user["timestamp"]

                    # Ensure timestamp is converted properly
                    if isinstance(timestamp, str):
                        timestamp = datetime.fromisoformat(timestamp)  # Convert from ISO string
                    elif isinstance(timestamp, int):
                        timestamp = datetime.fromtimestamp(timestamp, tz=timezone.utc)  # Convert from UNIX timestamp

                    registration_data.append(timestamp.strftime("%Y-%m-%d"))
                except Exception as e:
                    print(f"Skipping invalid timestamp: {user['timestamp']} - Error: {e}")

        return jsonify({"dates": registration_data}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ------------------------------------- USERS COLLECTIONS ENDS HERE ----------------------------------------------


# ------------------------------------- TRAIN COLLECTIONS STARTS HERE ----------------------------------------------

trains_collection = db["trains"]

# Valid Train Statuses
VALID_STATUSES = {"Active", "Maintenance", "Out of Service"}  # Set of valid statuses

def validate_train_data(train_data):
    if train_data.get("status") not in VALID_STATUSES:
        raise ValueError("Invalid train status. Must be 'Active', 'Maintenance', or 'Out of Service'.")



# Route to add a new train
@app.route("/add_train", methods=["POST"])
def add_train():
    data = request.json
    error = validate_train_data(data)
    
    if error:
        return jsonify({"error": error}), 400

    train_id = trains_collection.insert_one(data).inserted_id
    return jsonify({"message": "Train added successfully", "train_id": str(train_id)}), 201



# Route to update train status
@app.route("/update_train_status", methods=["POST"])
def update_train_status():
    data = request.json
    train_id = data.get("train_number")
    new_status = data.get("status")

    if not ObjectId.is_valid(train_id):
        return jsonify({"error": "Invalid train ID"}), 400

    if new_status not in VALID_STATUSES:
        return jsonify({"error": "Invalid status. Must be 'Active', 'Maintenance', or 'Out of Service'."}), 400

    result = trains_collection.update_one(
        {"_id": ObjectId(train_id)},
        {"$set": {"status": new_status}}
    )

    if result.matched_count == 0:
        return jsonify({"error": "Train not found"}), 404

    return jsonify({"message": "Train status updated successfully"}), 200



# Route to get all trains
@app.route("/get_trains", methods=["GET"])
def get_trains():
    trains = list(trains_collection.find({}, {"_id": 1, "train_name": 1, "train_number": 1, "capacity": 1, "status": 1}))
    for train in trains:
        train["_id"] = str(train["_id"])  # Convert ObjectId to string
    return jsonify(trains), 200



# Get available trains for booking

def get_available_trains(route_id):
    # Fetch all scheduled trains for the route with available seats
    scheduled_trains = db.train_schedule.find({
        "route_id": ObjectId(route_id),
        "status": "Scheduled",
        "available_seats": {"$gt": 0}
    })

    available_trains = []
    for train in scheduled_trains:
        train_info = db.trains_collection.find_one({
            "_id": train["train_id"],
            "status": "Active"
        })

        if train_info:
            available_trains.append({
                "train_id": str(train["_id"]),
                "train_name": train["train_name"],
                "departure_time": train["departure_time"],
                "arrival_time": train["arrival_time"],
                "available_seats": train["available_seats"],
                "current_fare": train["dynamic_fare"]["current_fare"]
            })
    
    return available_trains


@app.route("/get_available_trains", methods=["GET"])
def get_available_trains_route():
    route_id = request.args.get("route_id")
    available_trains = get_available_trains(route_id)
    return jsonify({"trains": available_trains})

# ------------------------------------- TRAIN COLLECTIONS ENDS HERE -----------------------------------------------------





# ===================================== BOOKING/TICKETING ==================================================


@app.route("/get_bookings", methods=["GET"])
def get_bookings():
    ticket_bookings = list(bookings_collection.find({}, {
        "_id": 1, "passenger_name": 1, "phone_number": 1, "route_name": 1, "train_name": 1, 
        "departure": 1, "arrival": 1, "seat_number": 1, "price": 1, "departure_time": 1, 
        "booking_date": 1, "payment_status": 1, "booking_status": 1  # Added missing fields
    }))
    
    # Convert ObjectId to string
    for booking in ticket_bookings:
        booking["_id"] = str(booking["_id"])

    return jsonify(ticket_bookings), 200


# ===============================================================================================================

def calculate_dynamic_fare(route, departure_time, available_seats, total_seats, station_name):
    """
    Calculate the fare based on dynamic pricing rules.
    """
    base_rate = route["base_rate"]  # Base fare from routes_collection
    stations = {s["station_name"]: s["fare_multiplier"] for s in route["stations"]}

    # Get distance multiplier
    distance_multiplier = stations.get(station_name, 1.0)  # Default to 1.0 if not found

    # Determine peak hour factor
    nigeria_time = pytz.timezone("Africa/Lagos")
    departure_time_local = departure_time.astimezone(nigeria_time)  # Convert to Nigeria timezone
    departure_hour = departure_time_local.hour  # Extract the hour

    # Peak hours: 7 AM - 9 AM and 5 PM - 7 PM
    peak_factor = 1.2 if (7 <= departure_hour <= 9 or 17 <= departure_hour <= 19) else 1.0

    # Determine demand factor based on seat availability
    seat_availability = available_seats / total_seats
    if seat_availability > 0.7:
        demand_factor = 1.0  # Normal price
    elif seat_availability > 0.3:
        demand_factor = 1.2  # Medium demand
    else:
        demand_factor = 1.5  # High demand

    # Calculate final fare
    final_fare = base_rate * distance_multiplier * peak_factor * demand_factor
    return round(final_fare, 2)



# def calculate_dynamic_fare(route, departure_time_dt, available_seats, total_seats, station_name):
#     """
#     Calculate the fare based on dynamic pricing rules.
#     """
#     base_rate = route["base_rate"]  # Base fare from routes_collection
#     stations = {s["station_name"]: s["fare_multiplier"] for s in route["stations"]}

#     # Get distance multiplier
#     distance_multiplier = stations.get(station_name, 1.0)  # Default to 1.0 if not found

#     # Determine peak hour factor
#     nigeria_time = pytz.timezone("Africa/Lagos")
#     departure_time_local = departure_time_dt.astimezone(nigeria_time)  # Convert to Nigeria timezone
#     departure_hour = departure_time_local.hour  # Extract the hour

#     # Peak hours: 7 AM - 9 AM and 5 PM - 7 PM
#     peak_factor = 1.2 if (7 <= departure_hour <= 9 or 17 <= departure_hour <= 19) else 1.0

#     # Determine demand factor based on seat availability
#     seat_availability = available_seats / total_seats
#     if seat_availability > 0.7:
#         demand_factor = 1.0  # Normal price
#     elif seat_availability > 0.3:
#         demand_factor = 1.2  # Medium demand
#     else:
#         demand_factor = 1.5  # High demand

#     # Calculate final fare
#     final_fare = base_rate * distance_multiplier * peak_factor * demand_factor
#     return round(final_fare, 2)

# ===============================================================================================================

@app.route("/get_departure_time", methods=["POST"])
def get_departure_time():
    data = request.json

    # Extract fields from request
    departure_date = data.get("departure_date")  # Selected departure date
    route_id = data.get("route_id")  # Selected route ID
    train_id = data.get("train_id")  # Selected train ID

    if not departure_date or not route_id or not train_id:
        return jsonify({"error": "Departure date, route ID, or train ID is missing"}), 400

    try:
        # Convert departure_date to a datetime object
        departure_date_dt = datetime.strptime(departure_date, "%Y-%m-%d")

        # Fetch the next available departure time for the selected date, route, and train
        train_schedule = train_schedules_collection.find_one({
            "train_id": ObjectId(train_id),
            "route_id": ObjectId(route_id),
            "departure_time": {
                "$gte": departure_date_dt,
                "$lt": departure_date_dt + timedelta(days=1)  # All times on the selected date
            }
        })

        if not train_schedule:
            return jsonify({"error": "No available departures for the selected date, route, and train."}), 404

        # Format departure_time as a string
        departure_time = train_schedule["departure_time"]
        if isinstance(departure_time, datetime):
            formatted_departure_time = departure_time.strftime("%Y-%m-%d %H:%M:%S")
        elif isinstance(departure_time, dict) and "$date" in departure_time:
            timestamp_ms = int(departure_time["$date"]["$numberLong"])
            formatted_departure_time = datetime.utcfromtimestamp(timestamp_ms / 1000).strftime("%Y-%m-%d %H:%M:%S")
        else:
            return jsonify({"error": "Invalid departure_time format in the database."}), 500

        return jsonify({
            "departure_time": formatted_departure_time
        })
    except ValueError:
        return jsonify({"error": "Invalid departure date format. Use 'YYYY-MM-DD'."}), 400


# ==================================================================

# Function to calculate fare

def update_train_fare(train_schedule):
    route = routes_collection.find_one({"_id": train_schedule["route_id"]})
    final_fare = calculate_dynamic_fare(
        route,
        train_schedule["departure_time"],
        train_schedule["available_seats"],
        route["train_capacity"],
        train_schedule["route_name"]
    )

    # Update the current fare in MongoDB
    train_schedules_collection.update_one(
        {"_id": train_schedule["_id"]},
        {"$set": {"dynamic_fare.current_fare": final_fare, "dynamic_fare.last_updated": datetime.utcnow()}}
    )

# =========================================================================

@app.route("/calculate_fare", methods=["POST"])
def calculate_fare():
    data = request.json
    print("Received data for fare calculation:", data)  # Debugging log

    # Extract fields from request
    departure = data.get("departure")
    departure_time = data.get("departure_time")  # Assigned departure time from the frontend

    # Convert train_id and route_id to ObjectId properly
    try:
        train_id = ObjectId(data["train_id"]) if ObjectId.is_valid(data["train_id"]) else data["train_id"]
        route_id = ObjectId(data["route_id"]) if ObjectId.is_valid(data["route_id"]) else data["route_id"]
    except Exception as e:
        return jsonify({"error": f"Invalid train_id or route_id: {str(e)}"}), 400

    # Fetch train schedule
    train_schedule = train_schedules_collection.find_one({"train_id": ObjectId(train_id)})
    if not train_schedule:
        return jsonify({"error": "Train schedule not found"}), 404

    # Fetch route details
    route = routes_collection.find_one({"_id": route_id})
    if not route:
        return jsonify({"error": "Route not found"}), 404

    # Convert departure_time to a datetime object
    try:
        departure_time_dt = datetime.strptime(departure_time, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        return jsonify({"error": "Invalid departure_time format. Use 'YYYY-MM-DD HH:MM:SS'."}), 400

    # Get available seats & total seats
    available_seats = train_schedule["available_seats"]
    total_seats = route["train_capacity"]

    # ✅ Pass `departure_time_dt` (as datetime object) to `calculate_dynamic_fare`
    calculated_fare = calculate_dynamic_fare(route, departure_time_dt, available_seats, total_seats, departure)

    return jsonify({
        "fare": calculated_fare,
        "departure_time": departure_time  # Return the assigned departure time
    })



# =========================================================================================
# Function to book a ticket


@app.route("/book_ticket", methods=["POST"])
def book_ticket():
    data = request.json

    # Extract fields from request
    passenger_name = data.get("passenger_name")
    phone_number = data.get("phone_number")
    route_name = data.get("route_name")
    departure = data.get("departure")
    departure_time_str = data.get("departure_time")  # Assigned departure time from the frontend (as string)
    arrival = data.get("arrival")
    seat_number = data.get("seat_number")

    # Convert departure_time string to a datetime object
    try:
        departure_time = datetime.strptime(departure_time_str, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        return jsonify({"error": "Invalid departure_time format. Use 'YYYY-MM-DD HH:MM:SS'."}), 400

    # Convert train_id and route_id to ObjectId properly
    try:
        train_id = ObjectId(data["train_id"]) if ObjectId.is_valid(data["train_id"]) else data["train_id"]
        route_id = ObjectId(data["route_id"]) if ObjectId.is_valid(data["route_id"]) else data["route_id"]
    except Exception as e:
        return jsonify({"error": f"Invalid train_id or route_id: {str(e)}"}), 400

    # Fetch train schedule
    train_schedule = train_schedules_collection.find_one({"train_id": ObjectId(train_id)})
    if not train_schedule:
        return jsonify({"error": "Train schedule not found"}), 404

    # Fetch route details
    route = routes_collection.find_one({"_id": route_id})
    if not route:
        return jsonify({"error": "Route not found"}), 404

    # Get available seats & total seats
    available_seats = train_schedule["available_seats"]
    total_seats = route["train_capacity"]

    # ✅ Pass `departure_time` (as datetime object) to `calculate_dynamic_fare`
    calculated_fare = calculate_dynamic_fare(route, departure_time, available_seats, total_seats, departure)

    # 🔹 **Check if the seat is available**
    seat_query = {
        "train_id": ObjectId(train_id),
        "seats.seat_number": seat_number,
        "seats.status": "available"
    }

    seat_update = {
        "$inc": {"available_seats": -1},
        "$set": {"seats.$.status": "booked"}
    }

    seat_update_result = train_schedules_collection.update_one(seat_query, seat_update)

    if seat_update_result.modified_count == 0:
        return jsonify({"error": f"Seat {seat_number} is already booked or does not exist."}), 400

    # Save booking
    booking_data = {
        "passenger_name": passenger_name,
        "phone_number": phone_number,
        "route_id": str(route_id),  # Store as string in MongoDB
        "route_name": train_schedule["route_name"],
        "train_id": str(train_id),  # Store as string in MongoDB
        "train_name": train_schedule["train_name"],
        "departure": departure,
        "arrival": arrival,
        "seat_number": seat_number,
        "price": calculated_fare,
        "departure_time": departure_time_str,  # Use the original departure_time string
        "booking_date": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),  # Current date and time
        "payment_status": "Paid"  # Add payment_status field with default value "pending"
    }
    booking_id = bookings_collection.insert_one(booking_data).inserted_id

    print(f"Booking successful! Booking ID: {booking_id}, Price: {calculated_fare}")

    # Convert booking_id to string for JSON serialization
    booking_data["_id"] = str(booking_id)

    return jsonify({
        "message": "Booking successful!",
        "booking_id": str(booking_id),
        "price": calculated_fare,
        "departure_time": departure_time_str,
        "booking_data": booking_data
    })



# =========================================================================================
@app.route('/debug_trains', methods=['GET'])
def debug_trains():
    train_schedules = list(db.train_schedules.find({}, {"_id": 0, "train_id": 1, "train_name": 1}))
    
    # Convert ObjectId to string for JSON response
    for train in train_schedules:
        train["train_id"] = str(train["train_id"])  # Ensure train_id is sent correctly
    
    return jsonify({"available_trains": train_schedules})


# ------------------------------------- BOOKING/TICKETING ENDS HERE -----------------------------------------------------




# ------------------------------------- ROUTE COLLECTIONS START HERE ----------------------------------------------------

routes_collection = db["routes"]


# Route to get all trains
@app.route("/get_routes", methods=["GET"])
def get_routes():
    routes = list(routes_collection.find({}, {"_id": 0}))  # Exclude MongoDB _id
    return jsonify(routes)



# Function to notify clients when routes change
def notify_clients():
    try:
        routes = list(routes_collection.find({}, {"_id": 0}))
        print("Broadcasting updated routes:", routes)  # Debugging print
        socketio.emit("update_routes", routes)
    except Exception as e:
        print("Error broadcasting routes:", e)


# # Example function to add a route (Triggers real-time update)

@app.route('/add_route', methods=['POST'])
def add_route():
    try:
        new_route = {
            "route_name": "New Test Route",
            "stations": [{"station_id": "STN004", "station_name": "Test Station", "distance_from_start_km": 50, "fare_multiplier": 1.3}],
            "distance_km": 300,
            "base_rate": 2000,
            "train_capacity": 150
        }
        
        # Print new route to check if it's being formed correctly
        print("Adding new route:", new_route)

        # Insert into MongoDB
        result = routes_collection.insert_one(new_route)
        
        # Print the inserted ID
        print("Inserted ID:", result.inserted_id)
        
        # Notify connected clients
        notify_clients()

        return jsonify({"message": "Route added", "inserted_id": str(result.inserted_id)}), 201

    except Exception as e:
        print("Error inserting route:", e)
        return jsonify({"error": str(e)}), 500




# ----------------------------------SEAT AVAILABILITY -------------------------------------------------------------------















if (__name__ == "__main__"):
    socketio.run(app, host="0.0.0.0", port=5009, debug=True)