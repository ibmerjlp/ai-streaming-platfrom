import re
from pydantic import BaseModel, EmailStr, field_validator

PASSWORD_REGEX = re.compile(
    r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
)

class UserCreate(BaseModel):
    email: EmailStr
    password: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        if not PASSWORD_REGEX.match(value):
            raise ValueError(
                "Password must be at least 8 characters long and include "
                "uppercase, lowercase, number, and special character"
            )
        return value

class UserOut(BaseModel):
    id: str
    email: EmailStr
    created_at: str
