import os
import tempfile
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from p2p_rates_service import database, main


@pytest.fixture
def client():
    db_fd, db_path = tempfile.mkstemp()
    os.close(db_fd)
    engine = create_engine(f"sqlite:///{db_path}", connect_args={"check_same_thread": False})
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    database.engine = engine
    database.SessionLocal = TestingSessionLocal
    database.Base.metadata.create_all(bind=engine)

    main.SessionLocal = TestingSessionLocal
    main.init_db = lambda: None

    with TestClient(main.app) as c:
        yield c

    os.remove(db_path)


def test_click_and_report(client):
    response = client.get("/click", params={"target_url": "https://example.com", "user_id": "user"}, follow_redirects=False)
    assert response.status_code == 307

    report = client.get("/report")
    assert report.status_code == 200
    assert report.json() == {"https://example.com": {"user": 1}}


def test_click_requires_target_url(client):
    response = client.get("/click", params={"user_id": "foo"})
    assert response.status_code == 422
