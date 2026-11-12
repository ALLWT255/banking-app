
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    verify_access_token
)


def test_password_hashing():
    password = "TestPassword123!"
    hashed = hash_password(password)

    assert hashed != password
    assert verify_password(password, hashed)
    assert not verify_password("WrongPassword123!", hashed)


def test_valid_jwt(monkeypatch):
    monkeypatch.setenv(
        "JWT_SECRET_KEY",
        "local-pytest-secret-only-not-for-production-2026"
    )

    token = create_access_token(4)

    assert verify_access_token(token) == 4


def test_invalid_jwt(monkeypatch):
    monkeypatch.setenv(
        "JWT_SECRET_KEY",
        "local-pytest-secret-only-not-for-production-2026"
    )

    assert verify_access_token("fake.token.value") is None
