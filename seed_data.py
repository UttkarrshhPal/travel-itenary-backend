# seed_data.py
from database import SessionLocal
import models

def seed_database():
    db = SessionLocal()
    
    try:
        # Create locations
        phuket_airport = models.Location(
            name="Phuket Airport",
            type=models.LocationType.AIRPORT,
            region=models.Region.PHUKET,
            description="Phuket International Airport",
            latitude=8.1132,
            longitude=98.3169
        )
        
        krabi_airport = models.Location(
            name="Krabi Airport",
            type=models.LocationType.AIRPORT,
            region=models.Region.KRABI,
            description="Krabi International Airport",
            latitude=8.0533,
            longitude=98.9198
        )
        
        marina_phuket = models.Location(
            name="Marina Phuket Resort",
            type=models.LocationType.HOTEL,
            region=models.Region.PHUKET,
            description="Luxury beachfront resort",
            latitude=7.8825,
            longitude=98.2910
        )
        
        krabi_resort = models.Location(
            name="Krabi Resort",
            type=models.LocationType.HOTEL,
            region=models.Region.KRABI,
            description="Beachfront resort in Krabi",
            latitude=8.0533,
            longitude=98.9198
        )

        phi_phi = models.Location(
            name="Phi Phi Islands",
            type=models.LocationType.ATTRACTION,
            region=models.Region.PHUKET,
            description="Famous island group",
            latitude=7.7407,
            longitude=98.7784
        )

        ao_nang = models.Location(
            name="Ao Nang Beach",
            type=models.LocationType.ATTRACTION,
            region=models.Region.KRABI,
            description="Popular beach in Krabi",
            latitude=8.0349,
            longitude=98.8173
        )

        railay = models.Location(
            name="Railay Beach",
            type=models.LocationType.ATTRACTION,
            region=models.Region.KRABI,
            description="Famous for rock climbing and beautiful beaches",
            latitude=8.0055,
            longitude=98.8370
        )

        db.add_all([phuket_airport, krabi_airport, marina_phuket, krabi_resort, phi_phi, ao_nang, railay])
        db.flush()

        # Create activities
        island_hopping = models.Activity(
            name="Phi Phi Island Hopping",
            description="Full day island hopping tour",
            region=models.Region.PHUKET,
            duration_hours=8,
            price=100.0,
            location_id=phi_phi.id
        )

        rock_climbing = models.Activity(
            name="Railay Beach Rock Climbing",
            description="Half day rock climbing experience",
            region=models.Region.KRABI,
            duration_hours=4,
            price=80.0,
            location_id=railay.id
        )

        four_islands = models.Activity(
            name="Four Islands Tour",
            description="Full day tour of Krabi's famous islands",
            region=models.Region.KRABI,
            duration_hours=6,
            price=90.0,
            location_id=ao_nang.id
        )

        db.add_all([island_hopping, rock_climbing, four_islands])
        db.flush()

        # Create recommended itineraries for both Phuket and Krabi
        for region, default_hotel, airport in [
            (models.Region.PHUKET, marina_phuket, phuket_airport),
            (models.Region.KRABI, krabi_resort, krabi_airport)
        ]:
            for nights in range(2, 9):
                itinerary = models.Itinerary(
                    name=f"{region.value} {nights}-Night Adventure",
                    region=region,
                    description=f"Recommended {nights}-night stay in {region.value}",
                    duration_nights=nights,
                    is_recommended=True
                )
                db.add(itinerary)
                db.flush()

                # Add accommodations
                for day in range(1, nights + 1):
                    accommodation = models.Accommodation(
                        itinerary_id=itinerary.id,
                        hotel_id=default_hotel.id,
                        day_number=day
                    )
                    db.add(accommodation)

                # Add transfers
                arrival_transfer = models.Transfer(
                    itinerary_id=itinerary.id,
                    day_number=1,
                    from_location_id=airport.id,
                    to_location_id=default_hotel.id,
                    transfer_type=models.TransferType.CAR,
                    duration_hours=1.0
                )
                departure_transfer = models.Transfer(
                    itinerary_id=itinerary.id,
                    day_number=nights + 1,
                    from_location_id=default_hotel.id,
                    to_location_id=airport.id,
                    transfer_type=models.TransferType.CAR,
                    duration_hours=1.0
                )
                db.add_all([arrival_transfer, departure_transfer])

                # Add default activity based on region
                default_activity = island_hopping if region == models.Region.PHUKET else four_islands
                activity = models.ItineraryActivity(
                    itinerary_id=itinerary.id,
                    activity_id=default_activity.id,
                    day_number=2
                )
                db.add(activity)

        db.commit()
        print("Database seeded successfully!")
        
    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {str(e)}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()