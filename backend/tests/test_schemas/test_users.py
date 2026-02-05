import uuid
import pytest
from pydantic import ValidationError
from backlog_app.schemas.user import UserCreate, UserRead, UserUpdate


def test_user_create_valid():
    data = {
        "email": "test@example.com",
        "password": "strongpassword123"
    }
    user = UserCreate(**data)
    assert user.email == data["email"]
    assert user.password == data["password"]


@pytest.mark.parametrize(
    "email, password",
    [
        ("not-an-email", "password123"),
        ("test@example.com", ""),
        ("", "password123"),
    ]
)
def test_user_create_invalid(email, password):
    with pytest.raises(ValidationError):
        UserCreate(email=email, password=password)


def test_user_update_valid():
    data = {
        "email": "update@example.com",
        "password": "newpassword"
    }
    user_update = UserUpdate(**data)
    assert user_update.email == data["email"]
    assert user_update.password == data["password"]


def test_user_read():
    user_id = uuid.uuid4()
    data = {
        "id": user_id,
        "email": "read@example.com",
        "is_active": True,
        "is_superuser": False,
        "is_verified": True,
    }
    user = UserRead(**data)
    assert user.id == user_id
    assert user.email == data["email"]
    assert user.is_active is True
    assert user.is_superuser is False
    assert user.is_verified is True
