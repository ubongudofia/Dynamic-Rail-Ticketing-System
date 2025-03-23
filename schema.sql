CREATE TABLE admins (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('superadmin', 'manager') NOT NULL DEFAULT 'manager',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    firstname VARCHAR(50) NOT NULL,
    lastname VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('passenger', 'admin') NOT NULL DEFAULT 'passenger',
    status ENUM('active', 'inactive', 'banned') NOT NULL DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE stations (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE trains (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) UNIQUE NOT NULL,
    seat_capacity INT NOT NULL CHECK(seat_capacity > 0)
);

CREATE TABLE schedules (
    id INT PRIMARY KEY AUTO_INCREMENT,
    train_id INT NOT NULL,
    departure_station_id INT NOT NULL,
    arrival_station_id INT NOT NULL,
    departure_time TIME NOT NULL,
    arrival_time TIME NOT NULL,
    FOREIGN KEY (train_id) REFERENCES trains(id) ON DELETE CASCADE,
    FOREIGN KEY (departure_station_id) REFERENCES stations(id) ON DELETE CASCADE,
    FOREIGN KEY (arrival_station_id) REFERENCES stations(id) ON DELETE CASCADE
);

CREATE TABLE train_tracking (
    id INT PRIMARY KEY AUTO_INCREMENT,
    schedule_id INT NOT NULL,
    train_id INT NOT NULL,
    current_station_id INT,
    status ENUM('on_time', 'delayed', 'arrived', 'cancelled') NOT NULL DEFAULT 'on_time',
    expected_arrival_time TIME NOT NULL,
    actual_arrival_time TIME NULL,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (schedule_id) REFERENCES schedules(id) ON DELETE CASCADE,
    FOREIGN KEY (train_id) REFERENCES trains(id) ON DELETE CASCADE,
    FOREIGN KEY (current_station_id) REFERENCES stations(id) ON DELETE SET NULL
);

CREATE TABLE seats (
    id INT PRIMARY KEY AUTO_INCREMENT,
    schedule_id INT NOT NULL,
    seat_number INT NOT NULL,
    status ENUM('available', 'booked') NOT NULL DEFAULT 'available',
    FOREIGN KEY (schedule_id) REFERENCES schedules(id) ON DELETE CASCADE,
    UNIQUE(schedule_id, seat_number) -- Prevents duplicate seat bookings
);

CREATE TABLE tickets (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    schedule_id INT NOT NULL,
    seat_number INT NOT NULL,
    fare DECIMAL(10,2) NOT NULL CHECK(fare >= 0),
    booking_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    payment_status ENUM('unpaid', 'paid', 'cancelled') NOT NULL DEFAULT 'unpaid',
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (schedule_id) REFERENCES schedules(id) ON DELETE CASCADE,
    UNIQUE(schedule_id, seat_number) -- Prevents duplicate seat bookings
);

CREATE TABLE payments (
    id INT PRIMARY KEY AUTO_INCREMENT,
    ticket_id INT NOT NULL,
    amount DECIMAL(10,2) NOT NULL CHECK(amount >= 0),
    payment_method ENUM('card', 'cash', 'bank_transfer') NOT NULL,
    payment_status ENUM('pending', 'completed', 'failed', 'refunded') NOT NULL DEFAULT 'pending',
    transaction_id VARCHAR(100) UNIQUE NULL,
    payment_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (ticket_id) REFERENCES tickets(id) ON DELETE CASCADE
);






















































-- CREATE TABLE admins (
--     id INTEGER PRIMARY KEY AUTOINCREMENT,
--     username TEXT UNIQUE NOT NULL,
--     password_hash TEXT NOT NULL,
--     role TEXT CHECK(role IN ('superadmin', 'manager')) NOT NULL DEFAULT 'manager',
--     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
-- );

-- CREATE TABLE users (
--     id INTEGER PRIMARY KEY AUTOINCREMENT,
--     firstname TEXT NOT NULL,
--     lastname TEXT NOT NULL,
--     email TEXT UNIQUE NOT NULL,
--     phone TEXT UNIQUE NOT NULL,
--     password_hash TEXT NOT NULL,
--     role TEXT CHECK(role IN ('passenger', 'admin')) NOT NULL DEFAULT 'passenger',
--     status TEXT CHECK(status IN ('active', 'inactive', 'banned')) NOT NULL DEFAULT 'active',
--     timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
-- );

-- CREATE TABLE stations (
--     id INTEGER PRIMARY KEY AUTOINCREMENT,
--     name TEXT UNIQUE NOT NULL
-- );

-- CREATE TABLE trains (
--     id INTEGER PRIMARY KEY AUTOINCREMENT,
--     name TEXT UNIQUE NOT NULL,
--     seat_capacity INTEGER NOT NULL
-- );

-- CREATE TABLE train_tracking (
--     id INTEGER PRIMARY KEY AUTOINCREMENT,
--     schedule_id INTEGER NOT NULL,
--     train_id INTEGER NOT NULL,
--     current_station_id INTEGER,
--     status TEXT CHECK(status IN ('on_time', 'delayed', 'arrived', 'cancelled')) NOT NULL DEFAULT 'on_time',
--     expected_arrival_time TIME NOT NULL,
--     actual_arrival_time TIME,
--     last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
--     FOREIGN KEY (schedule_id) REFERENCES schedules(id),
--     FOREIGN KEY (train_id) REFERENCES trains(id),
--     FOREIGN KEY (current_station_id) REFERENCES stations(id)
-- );

-- CREATE TABLE schedules (
--     id INTEGER PRIMARY KEY AUTOINCREMENT,
--     train_id INTEGER NOT NULL,
--     departure_station_id INTEGER NOT NULL,
--     arrival_station_id INTEGER NOT NULL,
--     departure_time TIME NOT NULL,
--     arrival_time TIME NOT NULL,
--     FOREIGN KEY (train_id) REFERENCES trains(id),
--     FOREIGN KEY (departure_station_id) REFERENCES stations(id),
--     FOREIGN KEY (arrival_station_id) REFERENCES stations(id)
-- );

-- CREATE TABLE seats (
--     id INTEGER PRIMARY KEY AUTOINCREMENT,
--     schedule_id INTEGER NOT NULL,
--     seat_number INTEGER NOT NULL,
--     status TEXT CHECK(status IN ('available', 'booked')) NOT NULL DEFAULT 'available',
--     FOREIGN KEY (schedule_id) REFERENCES schedules(id),
--     UNIQUE(schedule_id, seat_number)
-- );

-- CREATE TABLE payments (
--     id INTEGER PRIMARY KEY AUTOINCREMENT,
--     ticket_id INTEGER NOT NULL,
--     amount DECIMAL(10,2) NOT NULL CHECK(amount >= 0),
--     payment_method TEXT CHECK(payment_method IN ('card', 'cash', 'bank_transfer')) NOT NULL,
--     payment_status TEXT CHECK(payment_status IN ('pending', 'completed', 'failed', 'refunded')) NOT NULL DEFAULT 'pending',
--     transaction_id TEXT UNIQUE,
--     payment_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
--     FOREIGN KEY (ticket_id) REFERENCES tickets(id)
-- );

-- CREATE TABLE tickets (
--     id INTEGER PRIMARY KEY AUTOINCREMENT,
--     schedule_id INTEGER NOT NULL,
--     passenger_name TEXT NOT NULL,
--     passenger_phone TEXT NOT NULL,
--     seat_number INTEGER NOT NULL,
--     fare DECIMAL(10,2) NOT NULL,
--     booking_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
--     payment_status TEXT CHECK(payment_status IN ('unpaid', 'paid', 'cancelled')) NOT NULL DEFAULT 'unpaid',
--     FOREIGN KEY (schedule_id) REFERENCES schedules(id),
--     UNIQUE(schedule_id, seat_number) -- Prevents duplicate seat bookings
-- );