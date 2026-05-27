import uuid
from fastapi import APIRouter, Depends, status
from app.db.database import get_db
from app.services.auth_service import AuthService
from app.schemas.user import UserCreate, UserOut, UserLogin

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.post(
    "/register",
    summary="Create a new user",
    description="Registers a user with email and password",
    status_code=status.HTTP_201_CREATED,
    response_model=UserOut
)
async def create_user(user: UserCreate, db=Depends(get_db)) -> UserOut:
    """Creates a user in the system"""

    auth_service = AuthService(db)

    return await auth_service.register_user(user.email, user.password)

@router.post(
    "/login",
    summary="Login a user",
    description="Authenticates a user with email and password",
    status_code=status.HTTP_200_OK,
    response_model=UserOut
)
async def login_user(user: UserLogin, db=Depends(get_db)) -> UserOut:
    """Authenticates a user in the system"""

    auth_service = AuthService(db)

    return await auth_service.authenticate_user(user.email, user.password)