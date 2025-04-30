from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, Text, Date, Time, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.sqltypes import TIMESTAMP
import enum

from .database import Base

class ActivityType(enum.Enum):
    SIGHTSEEING = "sightseeing"
    ADVENTURE = "adventure"
    RELAXATION = "relaxation"
    CULTURAL = "cultural"
    DINING = "dining"
    SHOPPING = "shopping"
    OTHER = "other"

class TransferType(enum.Enum):
    CAR = "car"
    BUS = "bus"
    FERRY = "ferry"
    FLIGHT = "flight"
    TRAIN = "train"
    WALKING = "walking"
    OTHER = "other"

class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    region = Column(String, nullable=False)
    description = Column(Text)
    
    # Relationships
    hotels = relationship("Hotel", back_populates="location")
    activities = relationship("Activity", back_populates="location")
    
    def __repr__(self):
        return f"<Location {self.name} in {self.region}>"

class Hotel(Base):
    __tablename__ = "hotels"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    location_id = Column(Integer, ForeignKey("locations.id"), nullable=False)
    rating = Column(Float, nullable=False)
    price_per_night = Column(Float, nullable=False)
    description = Column(Text)
    amenities = Column(Text)  # Comma-separated list of amenities
    
    # Relationships
    location = relationship("Location", back_populates="hotels")
    accommodations = relationship("Accommodation", back_populates="hotel")
    
    def __repr__(self):
        return f"<Hotel {self.name} ({self.rating}★)>"

class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    location_id = Column(Integer, ForeignKey("locations.id"), nullable=False)
    type = Column(Enum(ActivityType), nullable=False)
    duration_hours = Column(Float, nullable=False)
    price = Column(Float, nullable=False)
    description = Column(Text)
    
    # Relationships
    location = relationship("Location", back_populates="activities")
    itinerary_activities = relationship("ItineraryActivity", back_populates="activity")
    
    def __repr__(self):
        return f"<Activity {self.name} ({self.type.value})>"

class Itinerary(Base):
    __tablename__ = "itineraries"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    duration_nights = Column(Integer, nullable=False)
    region = Column(String, nullable=False)
    description = Column(Text)
    is_recommended = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    
    # Relationships
    accommodations = relationship("Accommodation", back_populates="itinerary", cascade="all, delete-orphan")
    transfers = relationship("Transfer", back_populates="itinerary", cascade="all, delete-orphan")
    itinerary_activities = relationship("ItineraryActivity", back_populates="itinerary", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Itinerary {self.name} ({self.duration_nights} nights)>"

class Accommodation(Base):
    __tablename__ = "accommodations"

    id = Column(Integer, primary_key=True, index=True)
    itinerary_id = Column(Integer, ForeignKey("itineraries.id"), nullable=False)
    hotel_id = Column(Integer, ForeignKey("hotels.id"), nullable=False)
    day_number = Column(Integer, nullable=False)  # Day 1, Day 2, etc.
    check_in_date = Column(Date, nullable=True)   # Optional for recommended itineraries
    check_out_date = Column(Date, nullable=True)  # Optional for recommended itineraries
    
    # Relationships
    itinerary = relationship("Itinerary", back_populates="accommodations")
    hotel = relationship("Hotel", back_populates="accommodations")
    
    def __repr__(self):
        return f"<Accommodation at {self.hotel.name} on Day {self.day_number}>"

class Transfer(Base):
    __tablename__ = "transfers"

    id = Column(Integer, primary_key=True, index=True)
    itinerary_id = Column(Integer, ForeignKey("itineraries.id"), nullable=False)
    day_number = Column(Integer, nullable=False)
    from_location = Column(String, nullable=False)
    to_location = Column(String, nullable=False)
    transfer_type = Column(Enum(TransferType), nullable=False)
    duration_hours = Column(Float, nullable=False)
    departure_time = Column(Time, nullable=True)  # Optional for recommended itineraries
    
    # Relationships
    itinerary = relationship("Itinerary", back_populates="transfers")
    
    def __repr__(self):
        return f"<Transfer from {self.from_location} to {self.to_location} on Day {self.day_number}>"

class ItineraryActivity(Base):
    __tablename__ = "itinerary_activities"

    id = Column(Integer, primary_key=True, index=True)
    itinerary_id = Column(Integer, ForeignKey("itineraries.id"), nullable=False)
    activity_id = Column(Integer, ForeignKey("activities.id"), nullable=False)
    day_number = Column(Integer, nullable=False)
    start_time = Column(Time, nullable=True)  # Optional for recommended itineraries
    
    # Relationships
    itinerary = relationship("Itinerary", back_populates="itinerary_activities")
    activity = relationship("Activity", back_populates="itinerary_activities")
    
    def __repr__(self):
        return f"<ItineraryActivity {self.activity.name} on Day {self.day_number}>"