from pymongo import MongoClient
import certifi
from pymongo import MongoClient
from werkzeug.security import generate_password_hash
from datetime import datetime, timezone, timedelta
import random



# MongoDB connection string
mongo_client = ""

try:
    # Connect to MongoDB with SSL certification
    client = MongoClient(mongo_client, tlsCAFile=certifi.where())  # Use MongoClient correctly

    # Get the database
    db = client.get_database("e_ticketing")

    # Check if connection is successful by listing collections
    collections = db.list_collection_names()

    print("✅ Successfully connected to MongoDB!")
    print("Collections in 'e_ticketing':", collections)
except Exception as e:
    print("❌ Error connecting to MongoDB:", e)




db = client.get_database("e_ticketing")

# Define bookings collection schema
bookings_collection = db["bookings"]

# Update existing bookings to add payment_status field
result = bookings_collection.update_many(
    {"payment_status": {"$exists": False}},  # Find documents where payment_status does not exist
    {"$set": {"payment_status": "Paid"}}  # Set payment_status to "pending"
)

print(f"Updated {result.modified_count} documents.")

















# from bson import ObjectId
# import time

# # Create or select database
# db = client.get_database("e_ticketing")





# trains_collection = db["trains"]
# routes_collection = db["routes"]
# train_schedules_collection = db["train_schedules"]

# # Fetch all active trains
# trains = list(trains_collection.find({"status": "Active"}))

# # Fetch route
# route = routes_collection.find_one({"route_name": "ABJ Town Express"})  # Update route name if different

# if not route:
#     print("Error: Route not found!")
#     exit()

# # Delete existing schedules (optional)
# train_schedules_collection.delete_many({"route_id": route["_id"]})  

# # Generate schedules
# for train in trains:
#     departure_time = datetime.utcnow() + timedelta(days=5)  # Next day's schedule
#     arrival_time = departure_time + timedelta(hours=2)  # Assuming 2-hour journey

#     schedule = {
#         "train_id": train["_id"],
#         "route_id": route["_id"],
#         "train_name": train["train_name"],
#         "route_name": route["route_name"],
#         "departure_time": departure_time,
#         "arrival_time": arrival_time,
#         "status": "Scheduled",
#         "available_seats": train["capacity"],
#         "dynamic_fare": {
#             "base_fare": route["base_rate"],
#             "current_fare": route["base_rate"] * 1.2,  # Example fare adjustment
#             "last_updated": datetime.utcnow(),
#         },
#         "seats": [{"seat_number": f"A{i+1}", "status": "available"} for i in range(train["capacity"])]
#     }

#     train_schedules_collection.insert_one(schedule)
#     print(f"Schedule created for {train['train_name']} on route {route['route_name']}")

# print("✅ Train schedules updated successfully!")




























# # Define bookings collection schema
# bookings_collection = db["bookings"]

# # Create a sample booking document
# sample_booking = {
#     "passenger_name": "John Doe",
#     "phone_number": "0804567890",
#     "route_id": ObjectId("67d9df0dc6c0c5606c48c4b3"),  # Replace with actual route ObjectId
#     "route_name": "ABJ Town Express",
#     "train_id": ObjectId("67d4e81a61abe421d4140d5f"),  # Replace with actual train ObjectId
#     "train_name": "Express A",
#     "departure": "Area One",
#     "arrival": "Nyanya",  # Current timestamp for departure
#     "seat_number": "A1",
#     "price": 3240,  # Dynamically calculated fare
#     "departure_time": datetime.utcnow(),  # Current timestamp for departure
#     "booking_date": datetime.utcnow(),  # Current timestamp for booking
    
# }

# # Insert sample booking (only if collection is empty)
# if bookings_collection.count_documents({}) == 0:
#     bookings_collection.insert_one(sample_booking)
#     print("Sample booking added!")

# # Create indexes for faster queries
# bookings_collection.create_index([("route_id", 1)])
# bookings_collection.create_index([("train_id", 1)])
# bookings_collection.create_index([("departure_time", 1)])
# bookings_collection.create_index([("phone_number", 1)])

# print("Bookings collection created successfully with route_id and train_id!")



























# # Collections
# trains_collection = db["trains"]
# routes_collection = db["routes"]
# train_schedules_collection = db["train_schedules"]

# # Fetch all active trains
# active_trains = trains_collection.find({"status": "Active"})

# for train in active_trains:
#     train_id = train["_id"]
#     capacity = int(train["capacity"])  # Convert capacity to int

#     # Generate seat numbers (e.g., A1, A2, A3...)
#     seats = [{"seat_number": f"A{i+1}", "status": "available"} for i in range(capacity)]

#     # Update train_schedule collection
#     train_schedules_collection.update_one(
#         {"train_id": train_id},
#         {"$set": {"seats": seats, "available_seats": capacity}}, upsert=True    # Upsert if not found
#     )

# print("Seats added successfully!")





















# # Default train speed (km/h)
# DEFAULT_TRAIN_SPEED_KMH = 80

# def create_train_schedule():
#     # Fetch an active train
#     train = trains_collection.find_one({"status": "Active"})
#     if not train:
#         print("No active trains available.")
#         return

#     # Fetch a random route
#     route = routes_collection.aggregate([{"$sample": {"size": 1}}]).next()
#     if not route:
#         print("No routes available.")
#         return

#     # Estimate travel time (distance / speed)
#     travel_time_hours = route["distance_km"] / DEFAULT_TRAIN_SPEED_KMH

#     # Generate a random departure time within the next 24 hours
#     departure_time = datetime.utcnow() + timedelta(hours=random.randint(1, 24))
#     arrival_time = departure_time + timedelta(hours=travel_time_hours)

#     # Calculate dynamic fare
#     base_fare = route["base_rate"]
#     current_fare = base_fare * random.uniform(1.0, 1.5)  # Random fare multiplier (1.0x - 1.5x)

#     # Insert train schedule
#     schedule_data = {
#         "train_id": train["_id"],
#         "route_id": route["_id"],
#         "train_name": train["train_name"],
#         "route_name": route["route_name"],
#         "departure_time": departure_time,
#         "arrival_time": arrival_time,
#         "status": "Scheduled",
#         "available_seats": train["capacity"],  # Set initial available seats
#         "dynamic_fare": {
#             "base_fare": base_fare,
#             "current_fare": round(current_fare, 2),
#             "last_updated": datetime.utcnow()
#         }
#     }
#     schedule_id = train_schedules_collection.insert_one(schedule_data).inserted_id
#     print(f"Train Schedule Created! ID: {schedule_id}")

#     return schedule_id


# def book_ticket(schedule_id, passenger_name):
#     """Books a ticket if seats are available."""
#     schedule = train_schedules_collection.find_one({"_id": schedule_id})

#     if not schedule:
#         print("Schedule not found.")
#         return

#     if schedule["available_seats"] > 0:
#         # Decrease available seats
#         train_schedules_collection.update_one(
#             {"_id": schedule_id},
#             {"$inc": {"available_seats": -1}}
#         )

#         # Create booking entry
#         booking_data = {
#             "schedule_id": schedule_id,
#             "passenger_name": passenger_name,
#             "fare_paid": schedule["dynamic_fare"]["current_fare"],
#             "booking_time": datetime.utcnow(),
#             "status": "Confirmed"
#         }
#         bookings_collection.insert_one(booking_data)
#         print(f"Ticket booked for {passenger_name}. Remaining seats: {schedule['available_seats'] - 1}")
#     else:
#         print("No available seats for this schedule.")


# def cancel_booking(booking_id):
#     """Cancels a ticket and restores a seat."""
#     booking = bookings_collection.find_one({"_id": booking_id})

#     if not booking:
#         print("Booking not found.")
#         return

#     # Update schedule to restore available seat
#     train_schedules_collection.update_one(
#         {"_id": booking["schedule_id"]},
#         {"$inc": {"available_seats": 1}}
#     )

#     # Mark booking as canceled
#     bookings_collection.update_one(
#         {"_id": booking_id},
#         {"$set": {"status": "Canceled"}}
#     )
#     print("Booking canceled and seat restored.")


# # Example usage
# schedule_id = create_train_schedule()  # Creates a schedule
# if schedule_id:
#     book_ticket(schedule_id, "John Doe")  # Books a ticket














































# routes_collection = db["routes"]  # Collection name

# # Define the static route document (no train_id, no fixed dates)
# route_data = {
#     "route_name": "ABJ Town Express",
#     "stations": [
#         {
#             "station_id": "NYA001",
#             "station_name": "Nyanya",
#             "distance_from_start_km": 0,
#             "fare_multiplier": 1.0
#         },
#         {
#             "station_id": "ARA002",
#             "station_name": "Area One",
#             "distance_from_start_km": 130,
#             "fare_multiplier": 1.5
#         },
#         {
#             "station_id": "LUB003",
#             "station_name": "Lugbe",
#             "distance_from_start_km": 500,
#             "fare_multiplier": 2.0
#         }
#     ],
#     "distance_km": 500,
#     "base_rate": 1500,
#     "train_capacity": 200
# }

# # Insert the route data into MongoDB
# inserted_id = routes_collection.insert_one(route_data).inserted_id

# # Confirm insertion
# print(f"Route inserted with ID: {inserted_id}")




















# # Create or select users collection
# admins_collection = db["admin"]

# # Ensure email uniqueness
# admins_collection.create_index("email", unique=True)

# # Define the user document schema (sample user)
# admin_document = {
#     "firstname": "Bolu",
#     "lastname": "Mustapha",
#     "email": "admin@example.com",
#     "phone": "08067543543",
#     "password": generate_password_hash("qwerty12345"),  # Hashed password
#     "role": "admin",  # Default role
#     "status": "active",  # Account status
#     "profile_picture": None  # GridFS file ID (None by default)
# }

# # Insert sample user (if email is not already in database)
# try:
#     admins_collection.insert_one(admin_document)
#     print("User document created successfully!")
# except Exception as e:
#     print("User already exists or error:", e)




# Create or select trains collection

# trains_collection = db["trains"]

# # Define train collection schema (Informal enforcement)
# VALID_STATUSES = ["Active", "Maintenance", "Out of Service"]

# # Sample train data
# train_data = [
#     {
#         "train_name": "Express A",
#         "train_number": "101",
#         "capacity": 250,
#         "status": "Active"
#     },
#     {
#         "train_name": "Metro A",
#         "train_number": "102",
#         "capacity": 250,
#         "status": "Active"
#     },
#     {
#         "train_name": "Express B",
#         "train_number": "103",
#         "capacity": 250,
#         "status": "Active"
#     },
#     {
#         "train_name": "Metro B",
#         "train_number": "104",
#         "capacity": 250,
#         "status": "Active"
#     },
#     {
#         "train_name": "Express C",
#         "train_number": "105",
#         "capacity": 250,
#         "status": "Maintenance"
#     },
#     {
#         "train_name": "Metro C",
#         "train_number": "106",
#         "capacity": 250,
#         "status": "Out of Service"
#     }
# ]

# # Insert train data
# insert_result = trains_collection.insert_many(train_data)

# # Confirm insertion
# print(f"Inserted Train IDs: {insert_result.inserted_ids}")

# # Fetch and print all train records
# all_trains = trains_collection.find()
# for train in all_trains:
#     print(train)