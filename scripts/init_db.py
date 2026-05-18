import asyncio
import sys
from pathlib import Path

# Add project root to path to allow imports
sys.path.append(str(Path(__file__).parent.parent))

from backend.app.db.base_class import Base
from backend.app.db.session import engine
from backend.app.models import User, Task  # Import models to ensure they are registered

async def create_tables():
    print("Connecting to database...")
    async with engine.begin() as conn:
        print("Creating tables...")
        await conn.run_sync(Base.metadata.create_all)
    print("Done! Database tables created.")

if __name__ == "__main__":
    asyncio.run(create_tables())
