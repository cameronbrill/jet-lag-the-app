from __future__ import annotations

from datetime import UTC, datetime, timedelta

import bcrypt
from fastapi import APIRouter, HTTPException, status
import jwt
from pydantic import BaseModel, EmailStr, Field, field_validator
from sqlalchemy.exc import IntegrityError

from jetlag.api.deps import DbConn, SettingsDep
from jetlag.db.generated.users import AsyncQuerier as UserQuerier

router = APIRouter(prefix="/auth", tags=["auth"])

# bcrypt uses at most the first 72 UTF-8 bytes of the password; longer inputs are unsafe to accept silently.
BCRYPT_PASSWORD_MAX_UTF8_BYTES = 72
PASSWORD_TOO_LONG_FOR_BCRYPT_MSG = "Password must be 72 bytes or fewer (bcrypt limit)"

_FALLBACK_HASH: str = bcrypt.hashpw(b"_", bcrypt.gensalt()).decode()


class PasswordExceedsBcryptLimitError(Exception):
    """Raised when a password's UTF-8 encoding exceeds bcrypt's 72-byte limit (internal / defense in depth)."""


def _hash_password(password: str) -> str:
    if len(password.encode("utf-8")) > BCRYPT_PASSWORD_MAX_UTF8_BYTES:
        raise PasswordExceedsBcryptLimitError
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def _verify_password(password: str, password_hash: str) -> bool:
    return bcrypt.checkpw(password.encode(), password_hash.encode())


class SignupBody(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)

    @field_validator("password")
    @classmethod
    def password_fits_bcrypt(cls, value: str) -> str:
        if len(value.encode("utf-8")) > BCRYPT_PASSWORD_MAX_UTF8_BYTES:
            raise ValueError(PASSWORD_TOO_LONG_FOR_BCRYPT_MSG)
        return value


class LoginBody(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=8192)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


def _issue_token(settings: SettingsDep, subject: str) -> str:
    payload = {
        "sub": subject,
        "exp": datetime.now(tz=UTC) + timedelta(minutes=settings.access_token_expire_minutes),
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)


@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(conn: DbConn, settings: SettingsDep, body: SignupBody) -> TokenResponse:
    existing = await UserQuerier(conn).get_user_by_email(email=body.email)
    if existing is not None:
        raise HTTPException(status_code=409, detail="User exists")
    try:
        await UserQuerier(conn).create_user(email=body.email, password_hash=_hash_password(body.password))
    except IntegrityError:
        raise HTTPException(status_code=409, detail="User exists") from None
    except PasswordExceedsBcryptLimitError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=PASSWORD_TOO_LONG_FOR_BCRYPT_MSG,
        ) from None
    token = _issue_token(settings, body.email)
    return TokenResponse(access_token=token)


@router.post("/login")
async def login(conn: DbConn, settings: SettingsDep, body: LoginBody) -> TokenResponse:
    user = await UserQuerier(conn).get_user_by_email(email=body.email)
    candidate_hash = user.password_hash if user is not None else _FALLBACK_HASH
    valid = _verify_password(body.password, candidate_hash)
    if user is None or not valid:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = _issue_token(settings, body.email)
    return TokenResponse(access_token=token)
