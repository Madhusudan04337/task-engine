from typing import Any, Generic, List, Optional, Type, TypeVar
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.db.base_class import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    def __init__(self, model: Type[ModelType], db: AsyncSession):
        """
        Base class for data access logic.
        """
        self.model = model
        self.db = db

    async def get(self, id: Any) -> Optional[ModelType]:
        """
        Fetch a single record by ID.
        """
        query = select(self.model).where(self.model.id == id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_multi(self, *, skip: int = 0, limit: int = 100) -> List[ModelType]:
        """
        Fetch multiple records with pagination.
        """
        query = select(self.model).offset(skip).limit(limit)
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def create(self, *, obj_in: dict[str, Any]) -> ModelType:
        """
        Create a new record.
        """
        db_obj = self.model(**obj_in)
        self.db.add(db_obj)
        await self.db.commit()
        await self.db.refresh(db_obj)
        return db_obj

    async def update(self, *, db_obj: ModelType, obj_in: dict[str, Any]) -> ModelType:
        """
        Update an existing record.
        """
        for field, value in obj_in.items():
            setattr(db_obj, field, value)
        
        self.db.add(db_obj)
        await self.db.commit()
        await self.db.refresh(db_obj)
        return db_obj

    async def remove(self, *, id: Any) -> Optional[ModelType]:
        """
        Delete a record by ID.
        """
        obj = await self.get(id)
        if obj:
            await self.db.delete(obj)
            await self.db.commit()
        return obj
