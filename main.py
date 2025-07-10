# main.py
from fastapi import (
    FastAPI,
    Query,
    Depends,
    HTTPException,
    status,
    Request,
    Response,
    Cookie,
    Form,
)
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from database import SessionLocal, get_db
import models
from fastapi.middleware.cors import CORSMiddleware
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SECRET_KEY = "your-secret-key"  # Change this in production!
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Define Pydantic models BEFORE using them in endpoints
class UserRegister(BaseModel):
    username: str
    password: str
    full_name: str


class AccommodationCreate(BaseModel):
    hotel_id: int
    day_number: int


class TransferCreate(BaseModel):
    day_number: int
    from_location: str
    to_location: str
    transfer_type: str
    duration_hours: float


class ItineraryActivityCreate(BaseModel):
    activity_id: int
    day_number: int


class ItineraryCreate(BaseModel):
    name: str
    duration_nights: int
    region: str
    description: str
    is_recommended: bool = False
    accommodations: List[AccommodationCreate]
    transfers: List[TransferCreate]
    itinerary_activities: List[ItineraryActivityCreate]


# In-memory user database (replace with actual database in production)
users_db = {
    "testuser": {
        "username": "testuser",
        "full_name": "Test User",
        "hashed_password": pwd_context.hash("testpass"),
        "role": "user",
    },
    "admin": {
        "username": "admin",
        "full_name": "Admin User",
        "hashed_password": pwd_context.hash("adminpass"),
        "role": "admin",
    },
}


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db: Session, username: str):
    """Get user from database"""
    return db.query(models.User).filter(models.User.username == username).first()


def authenticate_user(db: Session, username: str, password: str):
    """Authenticate user from database"""
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user_from_token(
    token: str = Cookie(None), db: Session = Depends(get_db)  # Add db dependency
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if not token:
        raise credentials_exception
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    # Use database to get user
    user = get_user(db, username)
    if user is None:
        raise credentials_exception
    return user


app = FastAPI()

# Allow frontend dev server for local testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://travel-itenary-frontend.vercel.app/"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/register")
def register(user_data: UserRegister, db: Session = Depends(get_db)):
    logger.info(
        f"Registration attempt - Username: {user_data.username}, Full name: {user_data.full_name}"
    )

    try:
        # Check if username already exists
        existing_user = (
            db.query(models.User)
            .filter(models.User.username == user_data.username)
            .first()
        )

        if existing_user:
            logger.warning(f"Username already exists: {user_data.username}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered",
            )

        # Validate password
        if len(user_data.password) < 8:
            logger.warning(f"Password too short for user: {user_data.username}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password must be at least 8 characters long",
            )

        # Create new user
        hashed_password = get_password_hash(user_data.password)
        db_user = models.User(
            username=user_data.username,
            full_name=user_data.full_name,
            hashed_password=hashed_password,
            role="user",
        )

        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        logger.info(f"User registered successfully: {user_data.username}")

        return {
            "message": "User registered successfully",
            "username": db_user.username,
            "full_name": db_user.full_name,
        }
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"Registration error for {user_data.username}: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Registration failed: {str(e)}",
        )


# Update authentication functions to use database
def get_user(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def authenticate_user(db: Session, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


@app.post("/login")
def login(
    response: Response,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),  # Add this dependency
):
    # Use db instead of users_db
    user = authenticate_user(db, username, password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    # Use user object attributes instead of dictionary keys
    access_token = create_access_token(data={"sub": user.username, "role": user.role})
    response.set_cookie(
        key="token",
        value=access_token,
        httponly=True,
        secure=False,  # Set to True in production with HTTPS
        samesite="lax",
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        path="/",
    )
    return {"message": "Login successful"}


@app.post("/logout")
def logout(response: Response):
    response.delete_cookie(key="token", path="/")
    return {"message": "Logged out"}


@app.get("/me")
def read_users_me(current_user: models.User = Depends(get_current_user_from_token)):
    return {
        "username": current_user.username,
        "full_name": current_user.full_name,
        "role": current_user.role,
    }


# Example protected route
@app.get("/protected")
def protected_route(current_user: models.User = Depends(get_current_user_from_token)):
    return {"message": f"Hello, {current_user.username}! This is a protected route."}


# MCP Routes
@app.get("/mcp/recommended-itineraries/")
def get_recommended_itineraries(
    nights: int = Query(..., ge=2, le=8),
    region: Optional[str] = Query(None, enum=["Phuket", "Krabi"]),
):
    if not 2 <= nights <= 8:
        raise HTTPException(
            status_code=400, detail="Duration must be between 2 and 8 nights"
        )

    db = SessionLocal()
    try:
        query = db.query(models.Itinerary).filter(
            models.Itinerary.is_recommended == True,
            models.Itinerary.duration_nights == nights,
        )

        if region:
            query = query.filter(
                models.Itinerary.region == models.Region[region.upper()]
            )

        recommended = query.all()

        if not recommended:
            raise HTTPException(
                status_code=404,
                detail=f"No recommended itineraries found for {nights} nights"
                f"{f' in {region}' if region else ''}",
            )

        # Convert to dictionary with relationships
        result = []
        for itinerary in recommended:
            itinerary_dict = {
                "id": itinerary.id,
                "name": itinerary.name,
                "region": itinerary.region.value,
                "description": itinerary.description,
                "duration_nights": itinerary.duration_nights,
                "accommodations": [
                    {
                        "day_number": acc.day_number,
                        "hotel": {
                            "id": acc.hotel.id,
                            "name": acc.hotel.name,
                            "type": acc.hotel.type.value,
                        },
                    }
                    for acc in itinerary.accommodations
                ],
                "transfers": [
                    {
                        "day_number": t.day_number,
                        "from_location": t.from_location.name,
                        "to_location": t.to_location.name,
                        "transfer_type": t.transfer_type.value,
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
            result.append(itinerary_dict)

        return result
    finally:
        db.close()


# Regular itinerary routes
@app.post("/itineraries/")
def create_itinerary(itinerary: ItineraryCreate, db: Session = Depends(get_db)):
    try:
        # Create itinerary
        db_itinerary = models.Itinerary(
            name=itinerary.name,
            region=models.Region[itinerary.region.upper()],
            description=itinerary.description,
            duration_nights=itinerary.duration_nights,
            is_recommended=itinerary.is_recommended,
        )
        db.add(db_itinerary)
        db.flush()

        # Add accommodations
        for acc in itinerary.accommodations:
            accommodation = models.Accommodation(
                itinerary_id=db_itinerary.id,
                hotel_id=acc.hotel_id,
                day_number=acc.day_number,
            )
            db.add(accommodation)

        # Add transfers
        for transfer in itinerary.transfers:
            # Get location IDs based on names
            from_location = (
                db.query(models.Location).filter_by(name=transfer.from_location).first()
            )
            to_location = (
                db.query(models.Location).filter_by(name=transfer.to_location).first()
            )

            if not from_location or not to_location:
                raise HTTPException(status_code=400, detail="Invalid location names")

            db_transfer = models.Transfer(
                itinerary_id=db_itinerary.id,
                day_number=transfer.day_number,
                from_location_id=from_location.id,
                to_location_id=to_location.id,
                transfer_type=models.TransferType[transfer.transfer_type.upper()],
                duration_hours=transfer.duration_hours,
            )
            db.add(db_transfer)

        # Add activities
        for activity in itinerary.itinerary_activities:
            db_activity = models.ItineraryActivity(
                itinerary_id=db_itinerary.id,
                activity_id=activity.activity_id,
                day_number=activity.day_number,
            )
            db.add(db_activity)

        db.commit()
        db.refresh(db_itinerary)

        print(f"✅ Itinerary created (ID: {db_itinerary.id}): {itinerary.dict()}")
        return {"message": "Itinerary created successfully", "id": db_itinerary.id}
    except Exception as e:
        db.rollback()
        print(f"Error creating itinerary: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/itineraries/{itinerary_id}")
def get_itinerary(itinerary_id: int, db: Session = Depends(get_db)):
    try:
        itinerary = db.query(models.Itinerary).filter_by(id=itinerary_id).first()
        if not itinerary:
            raise HTTPException(status_code=404, detail="Itinerary not found")

        # Convert to dictionary with relationships
        result = {
            "id": itinerary.id,
            "name": itinerary.name,
            "region": itinerary.region.value,
            "description": itinerary.description,
            "duration_nights": itinerary.duration_nights,
            "accommodations": [
                {
                    "day_number": acc.day_number,
                    "hotel": {
                        "id": acc.hotel.id,
                        "name": acc.hotel.name,
                        "type": acc.hotel.type.value,
                    },
                }
                for acc in itinerary.accommodations
            ],
            "transfers": [
                {
                    "day_number": t.day_number,
                    "from_location": t.from_location.name,
                    "to_location": t.to_location.name,
                    "transfer_type": t.transfer_type.value,
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
        return result
    except Exception as e:
        print(f"Error getting itinerary: {e}")
        raise HTTPException(status_code=500, detail="Database error")


@app.get("/locations/")
def get_locations(db: Session = Depends(get_db)):
    try:
        locations = db.query(models.Location).all()
        return [
            {
                "id": loc.id,
                "name": loc.name,
                "type": loc.type.value,
                "region": loc.region.value,
                "description": loc.description,
                "latitude": loc.latitude,
                "longitude": loc.longitude,
            }
            for loc in locations
        ]
    except Exception as e:
        print(f"Error in get_locations: {e}")
        raise HTTPException(status_code=500, detail="Database connection error")


@app.get("/activities/")
def get_activities(
    region: Optional[str] = Query(None, enum=["Phuket", "Krabi"]),
    db: Session = Depends(get_db),
):
    try:
        query = db.query(models.Activity)
        if region:
            query = query.filter(
                models.Activity.region == models.Region[region.upper()]
            )
        activities = query.all()
        return [
            {
                "id": act.id,
                "name": act.name,
                "description": act.description,
                "region": act.region.value,
                "duration_hours": act.duration_hours,
                "price": act.price,
                "location": (
                    {
                        "id": act.location.id,
                        "name": act.location.name,
                        "type": act.location.type.value,
                    }
                    if act.location
                    else None
                ),
            }
            for act in activities
        ]
    except Exception as e:
        print(f"Error in get_activities: {e}")
        raise HTTPException(status_code=500, detail="Database connection error")
