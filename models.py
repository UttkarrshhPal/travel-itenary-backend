# models.py
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date, Enum, Boolean, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="user")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class LocationType(enum.Enum):
    CITY = "city"
    ATTRACTION = "attraction"
    HOTEL = "hotel"
    AIRPORT = "airport"

class TransferType(enum.Enum):
    CAR = "car"
    VAN = "van"
    BOAT = "boat"
    BUS = "bus"

class Region(enum.Enum):
    PHUKET = "Phuket"
    KRABI = "Krabi"

class Location(Base):
    __tablename__ = 'locations'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    type = Column(Enum(LocationType), nullable=False)
    region = Column(Enum(Region), nullable=False)
    description = Column(Text)
    latitude = Column(Float)
    longitude = Column(Float)

class Activity(Base):
    __tablename__ = 'activities'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    region = Column(Enum(Region), nullable=False)
    duration_hours = Column(Float, nullable=False)
    price = Column(Float)
    location_id = Column(Integer, ForeignKey('locations.id'))
    
    location = relationship("Location")

class Itinerary(Base):
    __tablename__ = 'itineraries'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    region = Column(Enum(Region), nullable=False)
    description = Column(Text)
    duration_nights = Column(Integer, nullable=False)
    is_recommended = Column(Boolean, default=False)
    
    accommodations = relationship("Accommodation", back_populates="itinerary")
    transfers = relationship("Transfer", back_populates="itinerary")
    activities = relationship("ItineraryActivity", back_populates="itinerary")

class Accommodation(Base):
    __tablename__ = 'accommodations'
    
    id = Column(Integer, primary_key=True)
    itinerary_id = Column(Integer, ForeignKey('itineraries.id'))
    hotel_id = Column(Integer, ForeignKey('locations.id'))
    day_number = Column(Integer, nullable=False)
    
    itinerary = relationship("Itinerary", back_populates="accommodations")
    hotel = relationship("Location")

class Transfer(Base):
    __tablename__ = 'transfers'
    
    id = Column(Integer, primary_key=True)
    itinerary_id = Column(Integer, ForeignKey('itineraries.id'))
    day_number = Column(Integer, nullable=False)
    from_location_id = Column(Integer, ForeignKey('locations.id'))
    to_location_id = Column(Integer, ForeignKey('locations.id'))
    transfer_type = Column(Enum(TransferType), nullable=False)
    duration_hours = Column(Float, nullable=False)
    
    itinerary = relationship("Itinerary", back_populates="transfers")
    from_location = relationship("Location", foreign_keys=[from_location_id])
    to_location = relationship("Location", foreign_keys=[to_location_id])

class ItineraryActivity(Base):
    __tablename__ = 'itinerary_activities'
    
    id = Column(Integer, primary_key=True)
    itinerary_id = Column(Integer, ForeignKey('itineraries.id'))
    activity_id = Column(Integer, ForeignKey('activities.id'))
    day_number = Column(Integer, nullable=False)
    
    itinerary = relationship("Itinerary", back_populates="activities")
    activity = relationship("Activity")