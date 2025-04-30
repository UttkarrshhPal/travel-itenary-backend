from fastapi import FastAPI, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from . import models, schemas, crud
from .database import engine, get_db
from .mcp_server import MCPServer
from .seed_data import seed_data

# Initialize FastAPI app
app = FastAPI(
    title="Travel Itinerary API",
    description="API for managing travel itineraries in Thailand",
    version="1.0.0"
)

# Create database tables and seed data on startup
@app.on_event("startup")
def startup_event():
    models.Base.metadata.create_all(bind=engine)
    seed_data()

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the Travel Itinerary API"}

# Itinerary endpoints
@app.post("/itineraries/", response_model=schemas.Itinerary, status_code=status.HTTP_201_CREATED)
def create_itinerary(itinerary: schemas.ItineraryCreate, db: Session = Depends(get_db)):
    """
    Create a new travel itinerary with accommodations, transfers, and activities.
    """
    return crud.create_itinerary(db=db, itinerary=itinerary)

@app.get("/itineraries/", response_model=List[schemas.ItineraryResponse])
def read_itineraries(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Get all travel itineraries with pagination.
    """
    itineraries = crud.get_itineraries(db, skip=skip, limit=limit)
    return itineraries

@app.get("/itineraries/{itinerary_id}", response_model=schemas.ItineraryDetailResponse)
def read_itinerary(itinerary_id: int, db: Session = Depends(get_db)):
    """
    Get a specific travel itinerary by ID.
    """
    db_itinerary = crud.get_itinerary(db, itinerary_id=itinerary_id)
    if db_itinerary is None:
        raise HTTPException(status_code=404, detail="Itinerary not found")
    return db_itinerary

# MCP Server endpoint
@app.post("/mcp/recommended-itineraries/", response_model=schemas.MCPResponse)
def get_recommended_itineraries(request: schemas.MCPRequest, db: Session = Depends(get_db)):
    """
    Get recommended itineraries based on the specified number of nights and optionally region.
    """
    mcp_server = MCPServer(db)
    return mcp_server.get_recommended_itinerary_response(request)

# Location endpoints
@app.get("/locations/", response_model=List[schemas.Location])
def read_locations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Get all locations with pagination.
    """
    locations = crud.get_locations(db, skip=skip, limit=limit)
    return locations

# Hotel endpoints
@app.get("/hotels/", response_model=List[schemas.Hotel])
def read_hotels(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Get all hotels with pagination.
    """
    hotels = crud.get_hotels(db, skip=skip, limit=limit)
    return hotels

# Activity endpoints
@app.get("/activities/", response_model=List[schemas.Activity])
def read_activities(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Get all activities with pagination.
    """
    activities = crud.get_activities(db, skip=skip, limit=limit)
    return activities