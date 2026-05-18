from datetime import timedelta
from typing import Optional
import uuid

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.core.security import create_access_token, get_password_hash, verify_password
from backend.app.repositories.user import UserRepository
from backend.app.schemas.user import UserCreate, Token


class AuthService:
    def __init__(self, db: AsyncSession):
        self.user_repo = UserRepository(db)

    async def register_user(self, user_in: UserCreate):
        """
        Register a new user after validating email uniqueness.
        """
        existing_user = await self.user_repo.get_by_email(user_in.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A user with this email already exists.",
            )
        
        user_data = user_in.model_dump()
        password = user_data.pop("password")
        user_data["hashed_password"] = get_password_hash(password)
        
        return await self.user_repo.create(obj_in=user_data)

    async def authenticate_user(self, email: str, password: str) -> Optional[Token]:
        """
        Authenticate a user and return an access token.
        """
        user = await self.user_repo.get_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            return None
        
        access_token = create_access_token(
            data={"sub": str(user.id), "role": user.role}
        )
        return Token(access_token=access_token, token_type="bearer")
