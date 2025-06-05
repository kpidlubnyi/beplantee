import pytest
from fastapi.testclient import TestClient
from app.services.auth_service import create_user, authenticate_user, get_user_by_username, get_user_by_email
from app.schemas.auth import UserCreate
from app.utils.security import verify_password

class TestAuthService:
    def test_create_user(self, db_session):
        """Test user creation with proper password hashing"""
        user_data = UserCreate(
            username="newuser",
            email="newuser@example.com",
            password="TestPass123!"
        )
        
        created_user = create_user(db_session, user_data)
        
        assert created_user.username == "newuser"
        assert created_user.email == "newuser@example.com"
        assert created_user.hashed_password != "TestPass123!"
        assert verify_password("TestPass123!", created_user.hashed_password)

    def test_get_user_by_username(self, db_session, sample_user):
        """Test retrieving user by username"""
        found_user = get_user_by_username(db_session, "testuser")
        assert found_user is not None
        assert found_user.id == sample_user.id
        
        not_found_user = get_user_by_username(db_session, "nonexistent")
        assert not_found_user is None

    def test_get_user_by_email(self, db_session, sample_user):
        """Test retrieving user by email"""
        found_user = get_user_by_email(db_session, "test@example.com")
        assert found_user is not None
        assert found_user.id == sample_user.id
        
        not_found_user = get_user_by_email(db_session, "nonexistent@example.com")
        assert not_found_user is None

    def test_authenticate_user_success(self, db_session):
        """Test successful user authentication"""
        user_data = UserCreate(
            username="authuser",
            email="auth@example.com",
            password="ValidPass123!"
        )
        created_user = create_user(db_session, user_data)
        
        authenticated_user = authenticate_user(db_session, "authuser", "ValidPass123!")
        assert authenticated_user is not None
        assert authenticated_user.id == created_user.id

    def test_authenticate_user_wrong_password(self, db_session):
        """Test authentication with wrong password"""
        user_data = UserCreate(
            username="authuser2",
            email="auth2@example.com",
            password="ValidPass123!"
        )
        create_user(db_session, user_data)
        
        authenticated_user = authenticate_user(db_session, "authuser2", "WrongPass123!")
        assert authenticated_user is None

    def test_authenticate_user_nonexistent(self, db_session):
        """Test authentication with nonexistent user"""
        authenticated_user = authenticate_user(db_session, "nonexistent", "password")
        assert authenticated_user is None

class TestAuthAPI:
    def test_register_success(self, client):
        """Test successful user registration via API"""
        user_data = {
            "username": "apiuser",
            "email": "api@example.com",
            "password": "ApiPass123!"
        }
        
        response = client.post("/auth/register", json=user_data)
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    def test_register_duplicate_username(self, client):
        """Test registration with duplicate username"""
        user_data = {
            "username": "duplicateuser",
            "email": "first@example.com",
            "password": "ValidPass123!"
        }
        client.post("/auth/register", json=user_data)
        
        duplicate_data = {
            "username": "duplicateuser",
            "email": "second@example.com", 
            "password": "ValidPass123!"
        }
        
        response = client.post("/auth/register", json=duplicate_data)
        
        assert response.status_code == 400
        assert "Username already registered" in response.json()["detail"]

    def test_register_duplicate_email(self, client):
        """Test registration with duplicate email"""
        user_data = {
            "username": "firstuser",
            "email": "duplicate@example.com",
            "password": "ValidPass123!"
        }
        client.post("/auth/register", json=user_data)
        
        duplicate_data = {
            "username": "seconduser",
            "email": "duplicate@example.com",
            "password": "ValidPass123!"
        }
        
        response = client.post("/auth/register", json=duplicate_data)
        
        assert response.status_code == 400
        assert "Email already registered" in response.json()["detail"]

    def test_register_invalid_password(self, client):
        """Test registration with invalid password"""
        user_data = {
            "username": "invalidpass",
            "email": "invalid@example.com",
            "password": "weak"
        }
        
        response = client.post("/auth/register", json=user_data)
        
        assert response.status_code == 422

    def test_login_success(self, client):
        """Test successful login via API"""
        user_data = {
            "username": "loginuser",
            "email": "login@example.com",
            "password": "LoginPass123!"
        }
        client.post("/auth/register", json=user_data)
        
        login_data = {
            "username": "loginuser",
            "password": "LoginPass123!"
        }
        
        response = client.post("/auth/login", data=login_data)
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    def test_login_wrong_credentials(self, client):
        """Test login with wrong credentials"""
        user_data = {
            "username": "wrongcreds",
            "email": "wrong@example.com",
            "password": "CorrectPass123!"
        }
        client.post("/auth/register", json=user_data)
        
        login_data = {
            "username": "wrongcreds",
            "password": "WrongPass123!"
        }
        
        response = client.post("/auth/login", data=login_data)
        
        assert response.status_code == 401
        assert "Incorrect username or password" in response.json()["detail"]

    def test_login_nonexistent_user(self, client):
        """Test login with nonexistent user"""
        login_data = {
            "username": "nonexistent",
            "password": "password"
        }
        
        response = client.post("/auth/login", data=login_data)
        
        assert response.status_code == 401