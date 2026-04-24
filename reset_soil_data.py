import sys
sys.path.insert(0, 'D:\\agri project new\\project agri')

from app import app, db, SoilData

with app.app_context():
    # Delete all existing soil data so it regenerates with location-based values
    deleted = SoilData.query.delete()
    db.session.commit()
    print(f"Deleted {deleted} soil records")
    print("Soil data will now be generated based on user location!")
    print("Different locations will get different crop recommendations!")
