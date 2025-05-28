import pytest
import os
import tempfile
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

from app.main import app
from app.database import get_db, Base
from app.models.user import User
from app.models.plant import Plant
from app.models.user_plant import UserPlant
from app.utils.security import create_access_token, get_password_hash

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_temp.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False},
    echo=False
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="session", autouse=True)
def create_test_database():
    """Create the test database tables once per session"""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)
    try:
        os.remove("./test_temp.db")
    except:
        pass

@pytest.fixture(scope="function")
def db_session():
    """Create a fresh database session for each test"""
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture(scope="function") 
def client(db_session):
    """Create a test client with database session override"""
    def override_get_db_for_test():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db_for_test
    
    with TestClient(app) as c:
        yield c
    
    app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
def sample_user(db_session):
    """Create a sample user for testing"""
    user = User(
        username="testuser",
        email="test@example.com",
        hashed_password=get_password_hash("testpassword123"),
        is_active=True,
        created_at=datetime.utcnow()
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user

@pytest.fixture
def sample_plant(db_session):
    """Create a sample plant for testing"""
    plant = Plant(
        common_name="Test Plant",
        scientific_name="Testus plantus",
        family="Testaceae",
        watering="Average",
        sunlight="Full sun",
        description="A test plant for testing purposes"
    )
    db_session.add(plant)
    db_session.commit()
    db_session.refresh(plant)
    return plant

@pytest.fixture
def sample_user_plant(db_session, sample_user, sample_plant):
    """Create a sample user plant for testing"""
    now = datetime.utcnow()
    user_plant = UserPlant(
        plant_id=sample_plant.id,
        owner_id=sample_user.id,
        name="My Test Plant",
        last_watering=now,
        last_sunfilling=now,
        image="default_plant.png",
        thumbnail="thumbnails/default_plant_thumbnail.png"
    )
    db_session.add(user_plant)
    db_session.commit()
    db_session.refresh(user_plant)
    return user_plant

@pytest.fixture
def auth_token(sample_user):
    """Create an authentication token for testing"""
    return create_access_token(data={"sub": sample_user.username})

@pytest.fixture
def auth_headers(auth_token):
    """Create authorization headers for testing"""
    return {"Authorization": f"Bearer {auth_token}"}

@pytest.fixture
def temp_upload_dir():
    """Create a temporary upload directory for testing"""
    temp_dir = tempfile.mkdtemp()
    os.makedirs(os.path.join(temp_dir, "thumbnails"), exist_ok=True)
    yield temp_dir
    import shutil
    shutil.rmtree(temp_dir, ignore_errors=True)

@pytest.fixture
def authenticated_user_data(sample_user):
    """Get user data for authenticated requests"""
    return {
        "id": sample_user.id,
        "username": sample_user.username,
        "email": sample_user.email
    }

@pytest.fixture
def create_auth_headers():
    """Factory function to create auth headers for any user"""
    def _create_headers(username):
        token = create_access_token(data={"sub": username})
        return {"Authorization": f"Bearer {token}"}
    return _create_headers