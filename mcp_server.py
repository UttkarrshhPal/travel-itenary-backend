# mcp_server.py
from fastapi import APIRouter, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from database import SessionLocal
import models
from typing import Optional

router = APIRouter()

@router.get("/recommended-itineraries")
def get_recommended_itineraries(
    nights: int = Query(..., ge=2, le=8),
    region: Optional[str] = None
):
    if not 2 <= nights <= 8:
        raise HTTPException(status_code=400, detail="Duration must be between 2 and 8 nights")
    
    db = SessionLocal()
    try:
        # Start with base query including eager loading of relationships
        query = db.query(models.Itinerary).options(
            joinedload(models.Itinerary.accommodations).joinedload(models.Accommodation.hotel),
            joinedload(models.Itinerary.activities).joinedload(models.ItineraryActivity.activity),
            joinedload(models.Itinerary.transfers)
        )

        # Apply filters
        query = query.filter(models.Itinerary.duration_nights == nights)
        
        if region:
            query = query.filter(models.Itinerary.region == region)
        
        # Get recommended itineraries
        recommended = query.filter(models.Itinerary.is_recommended == True)
        result = recommended.all()

        # If no recommended itineraries found, fall back to best matching ones
        if not result:
            # Find itineraries with most activities and good accommodation coverage
            query = query.join(models.ItineraryActivity).group_by(models.Itinerary.id)
            result = query.order_by(func.count(models.ItineraryActivity.activity_id).desc()).all()
            
        return result
    finally:
        db.close()