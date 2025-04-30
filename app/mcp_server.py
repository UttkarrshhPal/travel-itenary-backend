from sqlalchemy.orm import Session
from typing import List, Optional

from . import models, schemas, crud

class MCPServer:
    """
    MCP (Master Control Program) server for providing recommended itineraries
    based on the specified duration and optionally region.
    """
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_recommended_itineraries(self, nights: int, region: Optional[str] = None) -> List[models.Itinerary]:
        """
        Get recommended itineraries based on the specified number of nights and optionally region.
        
        Args:
            nights: Number of nights for the itinerary
            region: Optional region filter (e.g., "Phuket", "Krabi")
            
        Returns:
            List of recommended itineraries
        """
        return crud.get_recommended_itineraries(self.db, nights, region)
    
    def get_recommended_itinerary_response(self, request: schemas.MCPRequest) -> schemas.MCPResponse:
        """
        Get recommended itineraries based on the MCP request parameters.
        
        Args:
            request: MCP request with nights and optional region
            
        Returns:
            MCP response with recommended itineraries
        """
        itineraries = self.get_recommended_itineraries(request.nights, request.region)
        return schemas.MCPResponse(recommended_itineraries=itineraries)