import uuid, logging
from fastapi import HTTPException, status
from aiosqlite import IntegrityError
from app.core.security import hash_password, verify_password
from app.schemas.user import UserCreate, UserOut

logger = logging.getLogger(__name__)
class AuthService:
    def __init__(self, db):
        self.db = db

    async def register_user(self, email: str, password: str) -> UserOut:
        try:
            user_id = str(uuid.uuid4())
            hashed_password = hash_password(password)
            
            await self.db.execute("INSERT INTO users (id, email, hashed_password) VALUES (?, ?, ?)", (user_id, email, hashed_password))
            await self.db.commit()

            cursor = await self.db.execute("SELECT created_at FROM users WHERE id = ?", (user_id,))
            row = await cursor.fetchone()
            await cursor.close()

            return UserOut(id=user_id, email=email, created_at=row['created_at'])
        except IntegrityError as e:
            logger.warning(f"User registration failed - duplicate email: {e}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A user with this email already exists"
            )
        except Exception as e:
            logger.exception(f"Unexpected error during user registration: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An unexpected error occurred during registration"
            )

    async def authenticate_user(self, email: str, password: str) -> UserOut:
        cursor = await self.db.execute("SELECT id, email, hashed_password, is_active, created_at FROM users WHERE email = ?", (email,))
        user = await cursor.fetchone()
        await cursor.close()

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )
        
        if user['is_active'] == 0:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is inactive"
            )
        
        is_valid_password = verify_password(password, user['hashed_password'])

        if not is_valid_password:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )

        return UserOut(
            id=user['id'],
            email=user['email'],
            created_at=user['created_at']
        )