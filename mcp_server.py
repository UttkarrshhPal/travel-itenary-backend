# mcp_server.py
from fastapi import APIRouter, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
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
        base_query = (
            db.query(models.Itinerary)
            .options(
                joinedload(models.Itinerary.accommodations).joinedload(models.Accommodation.hotel),
                joinedload(models.Itinerary.activities).joinedload(models.ItineraryActivity.activity),
                joinedload(models.Itinerary.transfers)
            )
            .filter(
                models.Itinerary.duration_nights == nights,
                models.Itinerary.is_recommended == True
            )
        )

        results = []
        if region:
            reg = region.upper() if hasattr(models.Itinerary.region, 'value') else region
            itinerary = (
                base_query
                .filter(models.Itinerary.region == reg)
                .order_by(models.Itinerary.id.asc())
                .first()
            )
            if itinerary:
                results.append(itinerary)
        else:
            for reg in ["PHUKET", "KRABI"]:
                itinerary = (
                    base_query
                    .filter(models.Itinerary.region == reg)
                    .order_by(models.Itinerary.id.asc())
                    .first()
                )
                if itinerary:
                    results.append(itinerary)

        if not results:
            raise HTTPException(
                status_code=404,
                detail=f"No recommended itineraries found for {nights} nights"
                       f"{f' in {region}' if region else ''}"
            )

        # build result dictionaries as before
        final_result = []
        for itinerary in results:
            itinerary_dict = {
                "id": itinerary.id,
                "name": itinerary.name,
                "region": itinerary.region.value if hasattr(itinerary.region, 'value') else itinerary.region,
                "description": itinerary.description,
                "duration_nights": itinerary.duration_nights,
                "accommodations": [
                    {
                        "day_number": acc.day_number,
                        "hotel": {
                            "id": acc.hotel.id,
                            "name": acc.hotel.name,
                            "type": acc.hotel.type.value if hasattr(acc.hotel.type, "value") else acc.hotel.type,
                        },
                    }
                    for acc in itinerary.accommodations
                ],
                "transfers": [
                    {
                        "day_number": t.day_number,
                        "from_location": t.from_location.name,
                        "to_location": t.to_location.name,
                        "transfer_type": t.transfer_type.value if hasattr(t.transfer_type, "value") else t.transfer_type,
                        "duration_hours": t.duration_hours,
                    }
                    for t in itinerary.transfers
                ],
                "activities": [
                    {
                        "day_number": act.day_number,
                        "activity": {
                            "id": act.activity.id,
                            "name": act.activity.name,
                            "description": act.activity.description,
                            "duration_hours": act.activity.duration_hours,
                        },
                    }
                    for act in itinerary.activities
                ],
            }
            final_result.append(itinerary_dict)
        return final_result

    finally:
        db.close()