# from flask_sqlalchemy import SQLAlchemy
# from datetime import datetime 

# db = SQLAlchemy()

# class User(db.Model):
#     __tablename__ = "users"  # Ensure the table name matches your database
#     id = db.Column(db.Integer, primary_key=True)
#     firstname = db.Column(db.String(50), nullable=False)
#     lastname = db.Column(db.String(50), nullable=False)
#     email = db.Column(db.String(100), unique=True, nullable=False)
#     phone = db.Column(db.String(20), unique=True, nullable=False)
#     password_hash = db.Column(db.String(255), nullable=False)
#     role = db.Column(db.String(20), nullable=False, default="user")
#     status = db.Column(db.String(20), nullable=False, default="active")
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)
