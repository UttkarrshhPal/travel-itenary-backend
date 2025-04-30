from sqlalchemy.orm import Session
from . import models, database
from sqlalchemy import create_engine
from .database import SessionLocal

def seed_data():
    # Create the database tables
    models.Base.metadata.create_all(bind=database.engine)
    
    # Create a new session
    db = SessionLocal()
    
    try:
        # Check if data already exists
        if db.query(models.Location).count() > 0:
            print("Database already contains data. Skipping seed operation.")
            return
        
        print("Seeding database with initial data...")
        
        # Create locations
        phuket = models.Location(
            name="Phuket",
            region="Phuket",
            description="Phuket is Thailand's largest island and a popular beach destination known for its clear waters, white sand beaches, and vibrant nightlife."
        )
        
        patong = models.Location(
            name="Patong",
            region="Phuket",
            description="Patong is Phuket's most famous beach resort town with a vibrant nightlife scene and a 3-kilometer stretch of beach."
        )
        
        karon = models.Location(
            name="Karon",
            region="Phuket",
            description="Karon Beach is the second largest of Phuket's tourist beaches, featuring a long stretch of white sand beach."
        )
        
        kata = models.Location(
            name="Kata",
            region="Phuket",
            description="Kata is a scenic bay with a palm-lined beach and clear waters, popular for surfing during the monsoon season."
        )
        
        old_town = models.Location(
            name="Phuket Old Town",
            region="Phuket",
            description="Phuket Old Town is known for its charming historic district filled with colorful Sino-Portuguese buildings, cafes, and shops."
        )
        
        phi_phi = models.Location(
            name="Phi Phi Islands",
            region="Phuket",
            description="The Phi Phi Islands are an island group between Phuket and Krabi known for stunning beaches and limestone cliffs."
        )
        
        krabi_town = models.Location(
            name="Krabi Town",
            region="Krabi",
            description="Krabi Town is the capital of Krabi Province and a gateway to the region's national parks and islands."
        )
        
        ao_nang = models.Location(
            name="Ao Nang",
            region="Krabi",
            description="Ao Nang is a resort town in Thailand's Krabi Province with stunning limestone cliffs and access to offshore islands."
        )
        
        railay = models.Location(
            name="Railay Beach",
            region="Krabi",
            description="Railay Beach is a small peninsula between Krabi and Ao Nang, accessible only by boat and known for rock climbing."
        )
        
        koh_lanta = models.Location(
            name="Koh Lanta",
            region="Krabi",
            description="Koh Lanta is a laid-back island district in Krabi known for long beaches and a relaxed atmosphere."
        )
        
        db.add_all([phuket, patong, karon, kata, old_town, phi_phi, krabi_town, ao_nang, railay, koh_lanta])
        db.commit()
        
        # Create hotels
        # Phuket hotels
        phuket_hotels = [
            models.Hotel(
                name="Phuket Marriott Resort & Spa, Merlin Beach",
                location_id=phuket.id,
                rating=4.5,
                price_per_night=150.00,
                description="A luxury beachfront resort with multiple pools and restaurants.",
                amenities="Pool, Spa, Restaurant, WiFi, Beach access"
            ),
            models.Hotel(
                name="The Slate",
                location_id=phuket.id,
                rating=5.0,
                price_per_night=200.00,
                description="An art-inspired luxury resort with unique design and excellent facilities.",
                amenities="Pool, Spa, Restaurant, WiFi, Beach access, Fitness center"
            )
        ]
        
        # Patong hotels
        patong_hotels = [
            models.Hotel(
                name="Patong Resort Hotel",
                location_id=patong.id,
                rating=3.5,
                price_per_night=80.00,
                description="A mid-range hotel in the heart of Patong, walking distance to the beach and nightlife.",
                amenities="Pool, Restaurant, WiFi, Air conditioning"
            ),
            models.Hotel(
                name="Holiday Inn Resort Phuket",
                location_id=patong.id,
                rating=4.0,
                price_per_night=120.00,
                description="Family-friendly resort in Patong with multiple pools and activities.",
                amenities="Pool, Kids club, Restaurant, WiFi, Fitness center"
            )
        ]
        
        # Karon hotels
        karon_hotels = [
            models.Hotel(
                name="Hilton Phuket Arcadia Resort & Spa",
                location_id=karon.id,
                rating=4.5,
                price_per_night=170.00,
                description="A beachfront resort featuring 5 outdoor pools and extensive gardens.",
                amenities="Pool, Spa, Restaurant, WiFi, Beach access, Tennis courts"
            ),
            models.Hotel(
                name="Karon Sea Sands Resort & Spa",
                location_id=karon.id,
                rating=3.5,
                price_per_night=85.00,
                description="A comfortable resort just a short walk from Karon Beach.",
                amenities="Pool, Spa, Restaurant, WiFi"
            )
        ]
        
        # Kata hotels
        kata_hotels = [
            models.Hotel(
                name="The Shore at Katathani",
                location_id=kata.id,
                rating=5.0,
                price_per_night=300.00,
                description="An adults-only luxury resort with private pool villas overlooking Kata Noi Beach.",
                amenities="Private pools, Spa, Restaurant, WiFi, Beach access"
            ),
            models.Hotel(
                name="Kata Palm Resort & Spa",
                location_id=kata.id,
                rating=4.0,
                price_per_night=100.00,
                description="A tropical resort with multiple pools and palm trees.",
                amenities="Pool, Spa, Restaurant, WiFi"
            )
        ]
        
        # Phuket Old Town hotels
        old_town_hotels = [
            models.Hotel(
                name="The Memory at On On Hotel",
                location_id=old_town.id,
                rating=3.5,
                price_per_night=50.00,
                description="A historic hotel in the heart of Phuket Old Town, featured in the movie 'The Beach'.",
                amenities="WiFi, Restaurant, Air conditioning"
            ),
            models.Hotel(
                name="Casa Blanca Boutique Hotel",
                location_id=old_town.id,
                rating=4.0,
                price_per_night=70.00,
                description="A charming boutique hotel with Sino-Portuguese architecture.",
                amenities="WiFi, Restaurant, Air conditioning"
            )
        ]
        
        # Phi Phi hotels
        phi_phi_hotels = [
            models.Hotel(
                name="Phi Phi Island Village Beach Resort",
                location_id=phi_phi.id,
                rating=4.5,
                price_per_night=200.00,
                description="A beachfront resort with traditional Thai-style bungalows on Phi Phi Don Island.",
                amenities="Pool, Spa, Restaurant, WiFi, Beach access, Water sports"
            ),
            models.Hotel(
                name="Holiday Inn Resort Phi Phi Island",
                location_id=phi_phi.id,
                rating=4.0,
                price_per_night=180.00,
                description="Set on a private beach in Phi Phi Don Island with bungalow accommodations.",
                amenities="Pool, Restaurant, WiFi, Beach access, Spa"
            )
        ]
        
        # Krabi Town hotels
        krabi_town_hotels = [
            models.Hotel(
                name="The Brown Hotel",
                location_id=krabi_town.id,
                rating=3.5,
                price_per_night=45.00,
                description="A modern hotel in the center of Krabi Town with comfortable rooms.",
                amenities="WiFi, Restaurant, Air conditioning"
            ),
            models.Hotel(
                name="Dee Andaman Hotel",
                location_id=krabi_town.id,
                rating=3.0,
                price_per_night=35.00,
                description="A budget-friendly hotel with a pool in Krabi Town.",
                amenities="Pool, WiFi, Restaurant"
            )
        ]
        
        # Ao Nang hotels
        ao_nang_hotels = [
            models.Hotel(
                name="Centara Grand Beach Resort & Villas Krabi",
                location_id=ao_nang.id,
                rating=5.0,
                price_per_night=250.00,
                description="A luxury resort on a private bay accessible by boat from Ao Nang.",
                amenities="Pool, Spa, Restaurant, WiFi, Beach access, Water sports"
            ),
            models.Hotel(
                name="Aonang Villa Resort",
                location_id=ao_nang.id,
                rating=4.0,
                price_per_night=100.00,
                description="A beachfront resort in the heart of Ao Nang.",
                amenities="Pool, Restaurant, WiFi, Beach access"
            )
        ]
        
        # Railay hotels
        railay_hotels = [
            models.Hotel(
                name="Rayavadee",
                location_id=railay.id,
                rating=5.0,
                price_per_night=400.00,
                description="A luxury resort set on the edge of Krabi Marine National Park, surrounded by beaches and limestone cliffs.",
                amenities="Pool, Spa, Restaurant, WiFi, Beach access, Water sports"
            ),
            models.Hotel(
                name="Railay Princess Resort & Spa",
                location_id=railay.id,
                rating=3.5,
                price_per_night=90.00,
                description="A resort nestled between limestone cliffs with garden and pool views.",
                amenities="Pool, Spa, Restaurant, WiFi"
            )
        ]
        
        # Koh Lanta hotels
        koh_lanta_hotels = [
            models.Hotel(
                name="Pimalai Resort & Spa",
                location_id=koh_lanta.id,
                rating=5.0,
                price_per_night=300.00,
                description="A luxury beachfront resort on Koh Lanta with private pool villas.",
                amenities="Pool, Spa, Restaurant, WiFi, Beach access, Fitness center"
            ),
            models.Hotel(
                name="Lanta Sand Resort & Spa",
                location_id=koh_lanta.id,
                rating=4.0,
                price_per_night=120.00,
                description="A beachfront resort with comfortable rooms and a relaxing atmosphere.",
                amenities="Pool, Spa, Restaurant, WiFi, Beach access"
            )
        ]
        
        all_hotels = phuket_hotels + patong_hotels + karon_hotels + kata_hotels + old_town_hotels + phi_phi_hotels + krabi_town_hotels + ao_nang_hotels + railay_hotels + koh_lanta_hotels
        db.add_all(all_hotels)
        db.commit()
        
        # Create activities
        # Phuket activities
        phuket_activities = [
            models.Activity(
                name="Phuket City Tour",
                location_id=phuket.id,
                type=models.ActivityType.SIGHTSEEING,
                duration_hours=6.0,
                price=50.00,
                description="Explore the highlights of Phuket including viewpoints, temples, and cultural attractions."
            ),
            models.Activity(
                name="Elephant Sanctuary Visit",
                location_id=phuket.id,
                type=models.ActivityType.CULTURAL,
                duration_hours=4.0,
                price=80.00,
                description="Visit an ethical elephant sanctuary to learn about and interact with rescued elephants."
            ),
            models.Activity(
                name="Thai Cooking Class",
                location_id=phuket.id,
                type=models.ActivityType.CULTURAL,
                duration_hours=3.0,
                price=60.00,
                description="Learn to cook authentic Thai dishes with a professional chef."
            )
        ]
        
        # Patong activities
        patong_activities = [
            models.Activity(
                name="Patong Beach Day",
                location_id=patong.id,
                type=models.ActivityType.RELAXATION,
                duration_hours=6.0,
                price=0.00,
                description="Enjoy a day at Patong Beach with swimming and water sports options."
            ),
            models.Activity(
                name="Bangla Road Nightlife Tour",
                location_id=patong.id,
                type=models.ActivityType.OTHER,
                duration_hours=4.0,
                price=30.00,
                description="Experience the vibrant nightlife of Patong's famous Bangla Road."
            )
        ]
        
        # Phi Phi activities
        phi_phi_activities = [
            models.Activity(
                name="Phi Phi Islands Tour",
                location_id=phi_phi.id,
                type=models.ActivityType.SIGHTSEEING,
                duration_hours=8.0,
                price=100.00,
                description="Full-day speedboat tour of the Phi Phi Islands including Maya Bay and snorkeling spots."
            ),
            models.Activity(
                name="Sunset Dinner Cruise",
                location_id=phi_phi.id,
                type=models.ActivityType.DINING,
                duration_hours=3.0,
                price=70.00,
                description="Enjoy dinner on a boat while watching the sunset over the Phi Phi Islands."
            )
        ]
        
        # Ao Nang activities
        ao_nang_activities = [
            models.Activity(
                name="Four Islands Tour",
                location_id=ao_nang.id,
                type=models.ActivityType.ADVENTURE,
                duration_hours=7.0,
                price=65.00,
                description="Visit four beautiful islands by longtail boat with snorkeling opportunities."
            ),
            models.Activity(
                name="Rock Climbing in Ao Nang",
                location_id=ao_nang.id,
                type=models.ActivityType.ADVENTURE,
                duration_hours=4.0,
                price=85.00,
                description="Try rock climbing on the limestone cliffs with professional guides."
            )
        ]
        
        # Railay activities
        railay_activities = [
            models.Activity(
                name="Railay Beach Hopping",
                location_id=railay.id,
                type=models.ActivityType.RELAXATION,
                duration_hours=5.0,
                price=20.00,
                description="Explore the different beaches around Railay peninsula."
            ),
            models.Activity(
                name="Kayaking Around Railay",
                location_id=railay.id,
                type=models.ActivityType.ADVENTURE,
                duration_hours=3.0,
                price=40.00,
                description="Kayak around the karst formations and discover hidden lagoons and caves."
            )
        ]
        
        # Koh Lanta activities
        koh_lanta_activities = [
            models.Activity(
                name="Koh Lanta National Park",
                location_id=koh_lanta.id,
                type=models.ActivityType.SIGHTSEEING,
                duration_hours=5.0,
                price=25.00,
                description="Visit the national park at the southern tip of Koh Lanta."
            ),
            models.Activity(
                name="Scuba Diving Trip",
                location_id=koh_lanta.id,
                type=models.ActivityType.ADVENTURE,
                duration_hours=6.0,
                price=150.00,
                description="Experience scuba diving at some of Thailand's best dive sites."
            )
        ]
        
        all_activities = phuket_activities + patong_activities + phi_phi_activities + ao_nang_activities + railay_activities + koh_lanta_activities
        db.add_all(all_activities)
        db.commit()
        
        # Create recommended itineraries
        # 2-Night Phuket Itinerary
        phuket_2night = models.Itinerary(
            name="Quick Phuket Getaway",
            duration_nights=2,
            region="Phuket",
            description="A brief introduction to Phuket with a mix of beach time and cultural exploration.",
            is_recommended=True
        )
        
        # 3-Night Phuket Itinerary
        phuket_3night = models.Itinerary(
            name="Phuket Weekend Escape",
            duration_nights=3,
            region="Phuket",
            description="A perfect weekend in Phuket combining relaxation and adventure.",
            is_recommended=True
        )
        
        # 5-Night Phuket Itinerary
        phuket_5night = models.Itinerary(
            name="Phuket Explorer",
            duration_nights=5,
            region="Phuket",
            description="Dive deep into Phuket's beaches, culture, and nearby islands.",
            is_recommended=True
        )
        
        # 7-Night Phuket & Phi Phi Itinerary
        phuket_7night = models.Itinerary(
            name="Phuket & Phi Phi Adventure",
            duration_nights=7,
            region="Phuket",
            description="A week-long adventure combining the best of Phuket and the Phi Phi Islands.",
            is_recommended=True
        )
        
        # 2-Night Krabi Itinerary
        krabi_2night = models.Itinerary(
            name="Krabi Short Stay",
            duration_nights=2,
            region="Krabi",
            description="A quick visit to experience the highlights of Krabi's stunning landscape.",
            is_recommended=True
        )
        
        # 4-Night Krabi Itinerary
        krabi_4night = models.Itinerary(
            name="Krabi Beach & Adventure",
            duration_nights=4,
            region="Krabi",
            description="Explore Krabi's beaches, islands, and adventure activities.",
            is_recommended=True
        )
        
        # 6-Night Krabi & Koh Lanta Itinerary
        krabi_6night = models.Itinerary(
            name="Krabi & Koh Lanta Retreat",
            duration_nights=6,
            region="Krabi",
            description="Experience the best of Krabi Province including the laid-back island of Koh Lanta.",
            is_recommended=True
        )
        
        # 8-Night Krabi Explorer Itinerary
        krabi_8night = models.Itinerary(
            name="Complete Krabi Explorer",
            duration_nights=8,
            region="Krabi",
            description="An extensive tour of Krabi Province including Ao Nang, Railay, and Koh Lanta.",
            is_recommended=True
        )
        
        db.add_all([phuket_2night, phuket_3night, phuket_5night, phuket_7night, krabi_2night, krabi_4night, krabi_6night, krabi_8night])
        db.commit()
        
        # Add accommodations, transfers, and activities to itineraries
        
        # Phuket 2-night itinerary
        phuket_2night_accommodations = [
            models.Accommodation(
                itinerary_id=phuket_2night.id,
                hotel_id=patong_hotels[1].id,  # Holiday Inn Resort Phuket
                day_number=1
            ),
            models.Accommodation(
                itinerary_id=phuket_2night.id,
                hotel_id=patong_hotels[1].id,  # Holiday Inn Resort Phuket
                day_number=2
            )
        ]
        
        phuket_2night_transfers = [
            models.Transfer(
                itinerary_id=phuket_2night.id,
                day_number=1,
                from_location="Phuket Airport",
                to_location="Patong",
                transfer_type=models.TransferType.CAR,
                duration_hours=1.0
            ),
            models.Transfer(
                itinerary_id=phuket_2night.id,
                day_number=3,
                from_location="Patong",
                to_location="Phuket Airport",
                transfer_type=models.TransferType.CAR,
                duration_hours=1.0
            )
        ]
        
        phuket_2night_activities = [
            models.ItineraryActivity(
                itinerary_id=phuket_2night.id,
                activity_id=patong_activities[0].id,  # Patong Beach Day
                day_number=1
            ),
            models.ItineraryActivity(
                itinerary_id=phuket_2night.id,
                activity_id=patong_activities[1].id,  # Bangla Road Nightlife Tour
                day_number=1
            ),
            models.ItineraryActivity(
                itinerary_id=phuket_2night.id,
                activity_id=phuket_activities[0].id,  # Phuket City Tour
                day_number=2
            )
        ]
        
        db.add_all(phuket_2night_accommodations + phuket_2night_transfers + phuket_2night_activities)
        
        # Krabi 2-night itinerary
        krabi_2night_accommodations = [
            models.Accommodation(
                itinerary_id=krabi_2night.id,
                hotel_id=ao_nang_hotels[1].id,  # Aonang Villa Resort
                day_number=1
            ),
            models.Accommodation(
                itinerary_id=krabi_2night.id,
                hotel_id=ao_nang_hotels[1].id,  # Aonang Villa Resort
                day_number=2
            )
        ]
        
        krabi_2night_transfers = [
            models.Transfer(
                itinerary_id=krabi_2night.id,
                day_number=1,
                from_location="Krabi Airport",
                to_location="Ao Nang",
                transfer_type=models.TransferType.CAR,
                duration_hours=0.5
            ),
            models.Transfer(
                itinerary_id=krabi_2night.id,
                day_number=2,
                from_location="Ao Nang",
                to_location="Railay Beach",
                transfer_type=models.TransferType.FERRY,
                duration_hours=0.25
            ),
            models.Transfer(
                itinerary_id=krabi_2night.id,
                day_number=2,
                from_location="Railay Beach",
                to_location="Ao Nang",
                transfer_type=models.TransferType.FERRY,
                duration_hours=0.25
            ),
            models.Transfer(
                itinerary_id=krabi_2night.id,
                day_number=3,
                from_location="Ao Nang",
                to_location="Krabi Airport",
                transfer_type=models.TransferType.CAR,
                duration_hours=0.5
            )
        ]
        
        krabi_2night_activities = [
            models.ItineraryActivity(
                itinerary_id=krabi_2night.id,
                activity_id=ao_nang_activities[0].id,  # Four Islands Tour
                day_number=1
            ),
            models.ItineraryActivity(
                itinerary_id=krabi_2night.id,
                activity_id=railay_activities[0].id,  # Railay Beach Hopping
                day_number=2
            )
        ]
        
        db.add_all(krabi_2night_accommodations + krabi_2night_transfers + krabi_2night_activities)
        
        # Add more data for the other itineraries as well...
        # For brevity, we'll only add details for the 2-night itineraries in this example
        
        db.commit()
        print("Database seeded successfully!")
        
    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()