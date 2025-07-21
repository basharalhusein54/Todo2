from fastapi.testclient import TestClient
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.main import app as main_app
from app.db.database import Base
from app.main import app
from app.db.database import get_db
from app.crud.auth import authorize_user
url = settings.testing_database_url
connect_args = {"check_same_thread": False} if url.startswith("sqlite") else {}
engine = create_engine(url, connect_args=connect_args,poolclass=StaticPool)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#very important to use the same Base because all metadata there.
Base.metadata.create_all(engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

def override_authorize_user():
    return "admin"

main_app.dependency_overrides[get_db] = override_get_db
main_app.dependency_overrides[authorize_user] = override_authorize_user


client = TestClient(app)