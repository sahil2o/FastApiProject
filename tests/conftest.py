from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app import models
from app.oauth2 import create_access_token
from app.main import app
from app.config import settings
from app.database import get_db, Base

# SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:Admin@localhost:5432/fasyapi_test'

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

# Dependency


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)


@pytest.fixture
def test_user2(client):
    user_data = {"email": "hello3@gmail.com", "password": "abc123"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture
def test_user(client):
    user_data = {"email": "hello2@gmail.com", "password": "abc123"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": (test_user["id"])})


@pytest.fixture
def autherized_client(client, token):
    client.headers = {**client.headers, "Authorization": f"Bearer {token}"}
    return client


@pytest.fixture
def test_posts(test_user, session, test_user2):
    post_data = [
        {
            "title": "first title",
            "content": "first content",
            "owner_id": test_user["id"],
        },
        {
            "title": "second title",
            "content": "second content",
            "owner_id": test_user["id"],
        },
        {
            "title": "third title",
            "content": "third content",
            "owner_id": test_user["id"],
        },
        {
            "title": "third title",
            "content": "third content",
            "owner_id": test_user2["id"],
        },
    ]

    def create_post_model(post_data):
        return models.Post(**post_data)

    post_map = map(create_post_model, post_data)

    post = list(post_map)

    session.add_all(post)

    # session.add_all(
    #     [
    #         models.User(
    #             title="first title", content="first content", owner_id=test_user["id"]
    #         ),
    #         models.User(
    #             title="second title", content="second content", owner_id=test_user["id"]
    #         ),
    #         models.User(
    #             title="third title", content="third content", owner_id=test_user["id"]
    #         ),
    #     ]
    # )

    session.commit()

    posts = session.query(models.Post).all()
    return posts
