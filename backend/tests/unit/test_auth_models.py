from __future__ import annotations

from pydantic import ValidationError
import pytest

from jetlag.api.routes.auth import (
    BCRYPT_PASSWORD_MAX_UTF8_BYTES,
    PASSWORD_TOO_LONG_FOR_BCRYPT_MSG,
    LoginBody,
    PasswordExceedsBcryptLimitError,
    SignupBody,
    _hash_password,
)


def test_signup_body_accepts_valid_password() -> None:
    body = SignupBody(email="ok@example.com", password="password123")
    assert body.password == "password123"


def test_signup_body_rejects_short_password() -> None:
    with pytest.raises(ValidationError):
        SignupBody(email="ok@example.com", password="short")


def test_signup_body_rejects_73_ascii_bytes() -> None:
    with pytest.raises(ValidationError) as exc:
        SignupBody(email="ok@example.com", password="a" * 73)
    assert PASSWORD_TOO_LONG_FOR_BCRYPT_MSG in str(exc.value)


def test_signup_body_rejects_over_72_utf8_bytes_few_chars() -> None:
    password = "\U0001f600" * 36
    assert len(password.encode("utf-8")) > BCRYPT_PASSWORD_MAX_UTF8_BYTES
    with pytest.raises(ValidationError) as exc:
        SignupBody(email="ok@example.com", password=password)
    assert PASSWORD_TOO_LONG_FOR_BCRYPT_MSG in str(exc.value)


def test_login_body_rejects_empty_password() -> None:
    with pytest.raises(ValidationError):
        LoginBody(email="ok@example.com", password="")


def test_login_body_accepts_single_character_password() -> None:
    body = LoginBody(email="ok@example.com", password="x")
    assert body.password == "x"


def test_login_body_rejects_over_max_length() -> None:
    with pytest.raises(ValidationError):
        LoginBody(email="ok@example.com", password="p" * 8193)


def test_hash_password_raises_when_over_bcrypt_byte_limit() -> None:
    raw = "a" * 73
    with pytest.raises(PasswordExceedsBcryptLimitError):
        _hash_password(raw)
