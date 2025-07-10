# create_tables.py
from database import engine
import models

def create_tables():
    # This will create all tables defined in models.py
    models.Base.metadata.create_all(bind=engine)
    print("All tables created successfully!")
    
    # List all tables that were created
    print("\nCreated tables:")
    for table in models.Base.metadata.tables:
        print(f"  - {table}")

if __name__ == "__main__":
    create_tables()