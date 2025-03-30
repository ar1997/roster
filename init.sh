#!/bin/bash

echo "🚀 Building and starting containers..."
docker-compose up --build -d

echo "⏳ Waiting for backend to be ready..."
sleep 5

echo "👤 Creating initial admin user..."

docker-compose exec backend python3 -c "
from database import SessionLocal
from models import User, UserRole
from auth import get_password_hash

db = SessionLocal()
if not db.query(User).filter_by(username='admin').first():
    user = User(username='admin', hashed_password=get_password_hash('admin123'), role=UserRole.admin)
    db.add(user)
    db.commit()
    print('✅ Admin user created: admin / admin123')
else:
    print('⚠️ Admin user already exists')
db.close()
"

echo "✅ Done. Open http://localhost:5173 in your browser!"

