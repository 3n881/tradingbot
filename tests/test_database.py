from app.models.user import SessionLocal

db = SessionLocal()
try:
    db.execute("SELECT 1")
    print("Database connection successful!")
except Exception as e:
    print(f"Error: {e}")
finally:
    db.close()
