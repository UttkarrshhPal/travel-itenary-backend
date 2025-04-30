# Travel Itinerary Management System

A backend system for managing travel itineraries, built with FastAPI and SQLAlchemy.

## Features

- Database architecture for trip itineraries using SQLAlchemy
- RESTful API endpoints for creating and viewing itineraries
- MCP server that provides recommended itineraries based on duration
- Seed data for the Phuket and Krabi regions in Thailand

## Project Structure

```
travel_itinerary_system/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── database.py          # Database connection
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   ├── crud.py              # CRUD operations
│   ├── mcp_server.py        # MCP server for recommendations
│   └── seed_data.py         # Script to seed the database
├── requirements.txt         # Dependencies
└── README.md                # Documentation
```

## Setup and Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd travel_itinerary_system
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
uvicorn app.main:app --reload
```

5. Access the API documentation:
   - OpenAPI (Swagger UI): http://127.0.0.1:8000/docs
   - ReDoc: http://127.0.0.1:8000/redoc

## API Endpoints

### Itineraries

- `POST /itineraries/`: Create a new itinerary
- `GET /itineraries/`: List all itineraries
- `GET /itineraries/{itinerary_id}`: Get a specific itinerary

### MCP Server

- `POST /mcp/recommended-itineraries/`: Get recommended itineraries based on duration

### Supporting Endpoints

- `GET /locations/`: List all locations
- `GET /hotels/`: List all hotels
- `GET /activities/`: List all activities

## Sample API Usage

### Creating a New Itinerary

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/itineraries/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "Custom Phuket Trip",
  "duration_nights": 3,
  "region": "Phuket",
  "description": "A custom 3-night trip to Phuket",
  "is_recommended": false,
  "accommodations": [
    {
      "hotel_id": 1,
      "day_number": 1
    },
    {
      "hotel_id": 1,
      "day_number": 2
    },
    {
      "hotel_id": 2,
      "day_number": 3
    }
  ],
  "transfers": [
    {
      "day_number": 1,
      "from_location": "Phuket Airport",
      "to_location": "Hotel",
      "transfer_type": "car",
      "duration_hours": 1
    },
    {
      "day_number": 4,
      "from_location": "Hotel",
      "to_location": "Phuket Airport",
      "transfer_type": "car",
      "duration_hours": 1
    }
  ],
  "itinerary_activities": [
    {
      "activity_id": 1,
      "day_number": 1
    },
    {
      "activity_id": 2,
      "day_number": 2
    },
    {
      "activity_id": 3,
      "day_number": 3
    }
  ]
}'
```

### Getting Recommended Itineraries

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/mcp/recommended-itineraries/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "nights": 3,
  "region": "Phuket"
}'
```

## Database Schema

The database schema includes the following main entities:

- **Itinerary**: Represents a complete travel itinerary with accommodations, transfers, and activities
- **Location**: Represents a destination (e.g., Phuket, Krabi)
- **Hotel**: Represents a hotel accommodation
- **Activity**: Represents an excursion or activity
- **Accommodation**: Links an itinerary to hotels for specific days
- **Transfer**: Represents transportation between locations within an itinerary
- **ItineraryActivity**: Links activities to specific days in an itinerary

## Notes

- The database is automatically seeded with realistic data for the Phuket and Krabi regions in Thailand on application startup.
- The MCP server provides recommended itineraries based on the specified duration (number of nights) and optional region.