from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import List, Optional
from datetime import datetime

from . import models, schemas

# Itinerary CRUD operations
def create_itinerary(db: Session, itinerary: schemas.ItineraryCreate):
    # Create new itinerary
    db_itinerary = models.Itinerary(
        name=itinerary.name,
        duration_nights=itinerary.duration_nights,
        region=itinerary.region,
        description=itinerary.description,
        is_recommended=itinerary.is_recommended
    )
    db.add(db_itinerary)
    db.commit()
    db.refresh(db_itinerary)
    
    # Add accommodations
    for accommodation in itinerary.accommodations:
        db_accommodation = models.Accommodation(
            itinerary_id=db_itinerary.id,
            hotel_id=accommodation.hotel_id,
            day_number=accommodation.day_number,
            check_in_date=accommodation.check_in_date,
            check_out_date=accommodation.check_out_date
        )
        db.add(db_accommodation)
    
    # Add transfers
    for transfer in itinerary.transfers:
        db_transfer = models.Transfer(
            itinerary_id=db_itinerary.id,
            day_number=transfer.day_number,
            from_location=transfer.from_location,
            to_location=transfer.to_location,
            transfer_type=transfer.transfer_type,
            duration_hours=transfer.duration_hours,
            departure_time=transfer.departure_time
        )
        db.add(db_transfer)
    
    # Add activities
    for activity in itinerary.itinerary_activities:
        db_activity = models.ItineraryActivity(
            itinerary_id=db_itinerary.id,
            activity_id=activity.activity_id,
            day_number=activity.day_number,
            start_time=activity.start_time
        )
        db.add(db_activity)
    
    db.commit()
    db.refresh(db_itinerary)
    return db_itinerary

def get_itinerary(db: Session, itinerary_id: int):
    return db.query(models.Itinerary).filter(models.Itinerary.id == itinerary_id).first()

def get_itineraries(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Itinerary).offset(skip).limit(limit).all()

def get_recommended_itineraries(db: Session, nights: int, region: Optional[str] = None):
    query = db.query(models.Itinerary).filter(
        models.Itinerary.is_recommended == True,
        models.Itinerary.duration_nights == nights
    )
    
    if region:
        query = query.filter(models.Itinerary.region == region)
    
    return query.all()

# Location CRUD operations
def create_location(db: Session, location: schemas.LocationCreate):
    db_location = models.Location(**location.dict())
    db.add(db_location)
    db.commit()
    db.refresh(db_location)
    return db_location

def get_location(db: Session, location_id: int):
    return db.query(models.Location).filter(models.Location.id == location_id).first()

def get_locations(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Location).offset(skip).limit(limit).all()

# Hotel CRUD operations
def create_hotel(db: Session, hotel: schemas.HotelCreate):
    db_hotel = models.Hotel(**hotel.dict())
    db.add(db_hotel)
    db.commit()
    db.refresh(db_hotel)
    return db_hotel

def get_hotel(db: Session, hotel_id: int):
    return db.query(models.Hotel).filter(models.Hotel.id == hotel_id).first()

def get_hotels(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Hotel).offset(skip).limit(limit).all()

# Activity CRUD operations
def create_activity(db: Session, activity: schemas.ActivityCreate):
    db_activity = models.Activity(**activity.dict())
    db.add(db_activity)
    db.commit()
    db.refresh(db_activity)
    return db_activity

def get_activity(db: Session, activity_id: int):
    return db.query(models.Activity).filter(models.Activity.id == activity_id).first()

def get_activities(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Activity).offset(skip).limit(limit).all()