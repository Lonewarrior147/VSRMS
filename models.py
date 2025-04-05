from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin
from sqlalchemy.orm import backref,relationship
db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(30), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(20), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    address = db.Column(db.String(50), nullable=False)

    vehicles_owned = db.relationship('Vehicle', backref='owner', lazy=True)

class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    odo_reading = db.Column(db.Integer, nullable=False)
    license_plate = db.Column(db.String(20), unique=True, nullable=False)
    vin = db.Column(db.String(17), unique=True, nullable=False)

    vehicle_requires = db.relationship('Service', backref='vehicle_to_be_services', lazy=True)

class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'), nullable=False)
    bill_id = db.Column(db.Integer, nullable=True)
    description = db.Column(db.String(400), nullable=False)
    name = db.Column(db.String(50), nullable=False)
'''
    technician_id = db.Column(db.Integer, db.ForeignKey('technician.id'), unique=True)
    handled_by = db.relationship("Technician", backref=backref('assigned_service',uselist = False))

    toys= relationship("Parts", secondary=service_parts, back_populates="Service")

class Technician(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30),nullable=False)
    category = db.Column(db.String(30),nullable=False)
    phone = db.Column(db.String(10),nullable=False)
    available = db.Column(db.Boolean,nullable=False)

class Parts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    part_name = db.Column(db.String(30), nullable=False)
    qty_in_stock = db.Column(db.Integer,nullable=False)
    price_per_unit = db.Column(db.Integer,nullable=False)
    expiry_date = db.Column(db.datetime,nullable=False)

    services = relationship("Service", secondary=services_parts, back_populates="Parts")

service_parts = Table(
  "service_parts",
   Base.metadata,
   Column('service_id', ForeignKey('Service.id'), primary_key=True),
   Column('parts_id', ForeignKey('Parts.id'), primary_key=True)
)
'''
class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(30), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
