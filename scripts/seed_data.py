import asyncio
import sys
from pathlib import Path

# Add project root to path to allow imports
sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy import select
from backend.app.db.session import SessionLocal
from backend.app.models.user import User
from backend.app.core.security import get_password_hash
from backend.app.core.config import settings

async def seed_superuser():
    print("Seeding superuser...")
    async with SessionLocal() as session:
        # Check if user already exists
        query = select(User).where(User.email == settings.FIRST_SUPERUSER_EMAIL)
        result = await session.execute(query)
        user = result.scalar_one_or_none()

        if user:
            print(f"Superuser {settings.FIRST_SUPERUSER_EMAIL} already exists.")
            return

        # Create new superuser
        new_user = User(
            email=settings.FIRST_SUPERUSER_EMAIL,
            hashed_password=get_password_hash(settings.FIRST_SUPERUSER_PASSWORD),
            role="admin"
        )
        session.add(new_user)
        await session.commit()
        print(f"Superuser {settings.FIRST_SUPERUSER_EMAIL} created successfully.")

if __name__ == "__main__":
    asyncio.run(seed_superuser())
