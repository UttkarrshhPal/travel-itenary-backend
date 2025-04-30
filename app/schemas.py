from pydantic import BaseModel, Field
from typing import List, Optional, Union
from datetime import date, time
from enum import Enum

# Enum Schemas
class ActivityTypeEnum(str, Enum):
    SIGHTSEEING = "sightseeing"
    ADVENTURE = "adventure"
    RELAXATION = "relaxation"
    CULTURAL = "cultural"
    DINING = "dining"
    SHOPPING = "shopping"
    OTHER = "other"

class TransferTypeEnum(str, Enum):
    CAR = "car"
    BUS = "bus"
    FERRY = "ferry"
    FLIGHT = "flight"
    TRAIN = "train"
    WALKING = "walking"
    OTHER = "other"

# Location Schemas
class LocationBase(BaseModel):
    name: str
    region: str
    description: Optional[str] = None

class LocationCreate(LocationBase):
    pass

class Location(LocationBase):
    id: int

    class Config:
        orm_mode = True

# Hotel Schemas
class HotelBase(BaseModel):
    name: str
    location_id: int
    rating: float = Field(..., ge=0, le=5)
    price_per_night: float = Field(..., ge=0)
    description: Optional[str] = None
    amenities: Optional[str] = None

class HotelCreate(HotelBase):
    pass

class Hotel(HotelBase):
    id: int
    location: Location

    class Config:
        orm_mode = True

# Activity Schemas
class ActivityBase(BaseModel):
    name: str
    location_id: int
    type: ActivityTypeEnum
    duration_hours: float = Field(..., gt=0)
    price: float = Field(..., ge=0)
    description: Optional[str] = None

class ActivityCreate(ActivityBase):
    pass

class Activity(ActivityBase):
    id: int
    location: Location

    class Config:
        orm_mode = True

# Accommodation Schemas
class AccommodationBase(BaseModel):
    hotel_id: int
    day_number: int = Field(..., gt=0)
    check_in_date: Optional[date] = None
    check_out_date: Optional[date] = None

class AccommodationCreate(AccommodationBase):
    pass

class Accommodation(AccommodationBase):
    id: int
    hotel: Hotel

    class Config:
        orm_mode = True

# Transfer Schemas
class TransferBase(BaseModel):
    day_number: int = Field(..., gt=0)
    from_location: str
    to_location: str
    transfer_type: TransferTypeEnum
    duration_hours: float = Field(..., gt=0)
    departure_time: Optional[time] = None

class TransferCreate(TransferBase):
    pass

class Transfer(TransferBase):
    id: int

    class Config:
        orm_mode = True

# ItineraryActivity Schemas
class ItineraryActivityBase(BaseModel):
    activity_id: int
    day_number: int = Field(..., gt=0)
    start_time: Optional[time] = None

class ItineraryActivityCreate(ItineraryActivityBase):
    pass

class ItineraryActivity(ItineraryActivityBase):
    id: int
    activity: Activity

    class Config:
        orm_mode = True

# Itinerary Schemas
class ItineraryBase(BaseModel):
    name: str
    duration_nights: int = Field(..., ge=1)
    region: str
    description: Optional[str] = None
    is_recommended: bool = False

class ItineraryCreate(ItineraryBase):
    accommodations: List[AccommodationCreate]
    transfers: List[TransferCreate]
    itinerary_activities: List[ItineraryActivityCreate]

class Itinerary(ItineraryBase):
    id: int
    created_at: str
    accommodations: List[Accommodation]
    transfers: List[Transfer]
    itinerary_activities: List[ItineraryActivity]

    class Config:
        orm_mode = True

# Response Models
class ItineraryResponse(BaseModel):
    id: int
    name: str
    duration_nights: int
    region: str
    description: Optional[str] = None
    is_recommended: bool
    created_at: str
    
    class Config:
        orm_mode = True

class ItineraryDetailResponse(Itinerary):
    pass

# MCP Request/Response
class MCPRequest(BaseModel):
    nights: int = Field(..., ge=1, le=14)
    region: Optional[str] = None

class MCPResponse(BaseModel):
    recommended_itineraries: List[Itinerary]