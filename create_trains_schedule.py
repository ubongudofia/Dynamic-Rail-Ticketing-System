from pymongo import MongoClient
import certifi
from pymongo import MongoClient
from werkzeug.security import generate_password_hash
from datetime import datetime, timezone, timedelta
from bson import ObjectId

# MongoDB connection string
mongo_client = "mongodb+srv://udofiaubong10:qAWzNlJT6x2vSCdb@dsamessenger.tqp9u.mongodb.net"

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
train_schedules_collection = db["train_schedules"]

# Define active trains (extracted from your data)
active_trains = [
    {
        "train_id": "67d4e81a61abe421d4140d5f",
        "train_name": "Express A",
        "route_id": "67d9df0dc6c0c5606c48c4b3",
        "route_name": "ABJ Town Express"
    },
    {
        "train_id": "67d4e81a61abe421d4140d62",
        "train_name": "Metro B",
        "route_id": "67d9df0dc6c0c5606c48c4b3",
        "route_name": "ABJ Town Express"
    },
    {
        "train_id": "67d4e81a61abe421d4140d60",
        "train_name": "Metro A",
        "route_id": "67d9df0dc6c0c5606c48c4b3",
        "route_name": "ABJ Town Express"
    },
    {
        "train_id": "67d4e81a61abe421d4140d61",
        "train_name": "Express B",
        "route_id": "67d9df0dc6c0c5606c48c4b3",
        "route_name": "ABJ Town Express"
    }
]

# Define departure times (in "HH:MM" format)
departure_times = ["08:00", "10:00", "12:00", "14:00", "16:00", "18:00"]  # 8:00 AM, 10:00 AM, 12:00 PM, 2:00 PM, 4:00 PM, 6:00 PM

# Define the start date and number of days
start_date = datetime(2025, 3, 23)  # Start date: March 23, 2025
num_days = 30  # Number of days to create schedules for

# Insert schedules for each train and route
for train in active_trains:
    train_id = ObjectId(train["train_id"])
    route_id = ObjectId(train["route_id"])
    train_name = train["train_name"]
    route_name = train["route_name"]

    for day in range(num_days):
        for time_str in departure_times:
            # Parse the time string (e.g., "08:00") into hours and minutes
            hours, minutes = map(int, time_str.split(":"))

            # Calculate the departure time for the current day
            departure_time = start_date + timedelta(days=day, hours=hours, minutes=minutes)

            # Create the schedule document
            schedule = {
                "train_id": train_id,
                "route_id": route_id,
                "train_name": train_name,
                "route_name": route_name,
                "departure_time": departure_time,
                "available_seats": 3,  # Default number of seats (as per your data)
                "seats": [
                    {"seat_number": f"A{i}", "status": "available"} for i in range(1, 4)
                ],
                "status": "Scheduled",  # Default status
                "dynamic_fare": {
                    "base_fare": 1500,  # Default base fare
                    "current_fare": 1800.0,  # Default current fare
                    "last_updated": datetime.utcnow()  # Current timestamp
                }
            }

            # Insert the schedule into the database
            train_schedules_collection.insert_one(schedule)

print("Schedules added successfully!")