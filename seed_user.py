# seed_user.py
from app.db.session import SessionLocal
from app.db.models.user import User
from app.core.security import hash_password

db = SessionLocal()

user = User(
    email="admin@example.com",
    hashed_password=hash_password("password"),
    role="admin",
)

db.add(user)
db.commit()
db.close()

print("Admin user created")
