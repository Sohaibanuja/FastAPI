from app import models
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.main import app 
from app.config import settings
from app.database import get_db, Base
import pytest
from app.oauth2 import create_acces_token



# SQLACLHEMY_DATABASE_URL = 'postgresql://postgres:password123@localhost:5432/fastapi_test'
SQLACLHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'

engine = create_engine(SQLACLHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

#This whole code above can be copy paste and used for every other project it is the same if you are using sqlalchemy, postgress, and fastapi

@pytest.fixture()
def session():
    print("my session fixture ran")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):
    print("the client fixture ran")
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture()
def test_user2(client):
    user_data = { "email": "sohaib1@gmail.com",
                    "password" : "password123"}
    res = client.post("/users/", json= user_data)

    assert res.status_code == 201
    print(res.json())
    new_user = res.json()
    new_user['password'] = user_data["password"]
    print(new_user)
    return new_user

@pytest.fixture()
def test_user(client):
    user_data = { "email": "sohaib@gmail.com",
                    "password" : "password123"}
    res = client.post("/users/", json= user_data)

    assert res.status_code == 201
    print(res.json())
    new_user = res.json()
    new_user['password'] = user_data["password"]
    print(new_user)
    return new_user


@pytest.fixture()
def token(test_user):
    return create_acces_token({"user_id": test_user['id']})

@pytest.fixture()
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    print(client.headers)
    return client


@pytest.fixture()
def test_posts(test_user, session, test_user2):
    posts_data = [{
        "title": "first title",
        "content": "first content",
        "owner_id": test_user['id']
        },{
        "title": "second title",
        "content": "second content",
        "owner_id": test_user['id']
        },{
        "title": "third title",
        "content": "third content",
        "owner_id": test_user['id']
        },{
        "title": "third title",
        "content": "third content",
        "owner_id": test_user2['id']
        }]

    def create_post_model(post):
        return models.Post(**post)

    post_map = map(create_post_model, posts_data)
    map(create_post_model, posts_data)
    posts = list(post_map)


    session.add_all(posts)
    # session.add_all([
    #     models.Post(title="first title", content="first content", owner_id=test_user['id']),
    #     models.Post(title="second title", content="second content", owner_id=test_user['id']),
    #     models.Post(title="third title", content="third content", owner_id=test_user['id'])
    # ])

    session.commit()
    posts = session.query(models.Post).all()
    return posts