import pytest
from jose import jwt
from app import schemas
from app.config import settings


# def test_root(client):
#     res = client.get("/")
#     print(res.json().get('message'))
#     assert res.json().get('message') == 'Hello World'
#     assert res.status_code == 200


def test_create_user(client):
    res = client.post(
        "/users/", json={"email": "hello1@gmail.com", "password": "abc123"}
    )
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "hello1@gmail.com"
    assert res.status_code == 201


def test_user_login(test_user, client):
    res = client.post(
        "/login",
        data={"username": test_user["email"], "password": test_user["password"]},
    )
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(
        login_res.access_token, settings.secret_key, algorithms=[settings.algorithm]
    )
    id = payload.get("user_id")
    assert id == test_user["id"]
    assert login_res.token_type == "bearer"
    assert res.status_code == 200


@pytest.mark.parametrize(
    "username , password, status_code",
    [
        ("whateveremail@awd.com", "abc123", 403),
        ("hello2@gmail.com", "lalasda12", 403),
        (None, "abc123", 422),
        ("hello2@gmail.com", None, 422),
    ],
)
def test_incorrect_login(test_user, client, username, password, status_code):
    res = client.post("/login", data={"username": username, "password": password})

    assert res.status_code == status_code
