import pytest
from app.services.password_reset_service import verify_email_exists, reset_password_by_email
from app.utils.security import verify_password

class TestPasswordResetService:
    def test_verify_email_exists_success(self, db_session, sample_user):
        """Test email verification for existing user"""
        result = verify_email_exists(db_session, "test@example.com")
        
        assert result is True

    def test_verify_email_exists_not_found(self, db_session):
        """Test email verification for non-existent user"""
        result = verify_email_exists(db_session, "nonexistent@example.com")
        
        assert result is False

    def test_reset_password_by_email_success(self, db_session, sample_user):
        """Test successful password reset"""
        new_password = "NewPass123!"
        
        result = reset_password_by_email(db_session, "test@example.com", new_password)
        
        assert result is True
        
        db_session.refresh(sample_user)
        assert verify_password(new_password, sample_user.hashed_password)

    def test_reset_password_by_email_user_not_found(self, db_session):
        """Test password reset for non-existent user"""
        result = reset_password_by_email(db_session, "nonexistent@example.com", "NewPass123!")
        
        assert result is False

    def test_reset_password_by_email_weak_password(self, db_session, sample_user):
        """Test password reset with weak password"""
        weak_password = "weak"
        
        result = reset_password_by_email(db_session, "test@example.com", weak_password)
        
        assert result is True
        db_session.refresh(sample_user)
        assert verify_password(weak_password, sample_user.hashed_password)

class TestPasswordResetAPI:
    def test_verify_email_api_not_found(self, client):
        """Test POST /password-reset/verify-email with non-existent email"""
        request_data = {"email": "nonexistent@example.com"}
        
        response = client.post("/password-reset/verify-email", json=request_data)
        
        assert response.status_code == 404
        assert "User with this email address does not exist" in response.json()["detail"]

    def test_verify_email_api_invalid_email(self, client):
        """Test POST /password-reset/verify-email with invalid email format"""
        request_data = {"email": "invalid-email"}
        
        response = client.post("/password-reset/verify-email", json=request_data)
        
        assert response.status_code == 422

    def test_reset_password_api_success(self, client, sample_user):
        """Test POST /password-reset/reset with valid data"""
        request_data = {
            "email": "test@example.com",
            "password": "NewPass123!"
        }
        
        response = client.post("/password-reset/reset", json=request_data)
        
        assert response.status_code == 200
        data = response.json()
        assert "Password has been reset successfully" in data["message"]

    def test_reset_password_api_invalid_email(self, client):
        """Test POST /password-reset/reset with non-existent email"""
        request_data = {
            "email": "nonexistent@example.com",
            "password": "ValidPass123!"
        }
        
        response = client.post("/password-reset/reset", json=request_data)
        
        assert response.status_code == 400
        assert "Failed to reset password" in response.json()["detail"]

    def test_reset_password_api_weak_password(self, client, sample_user):
        """Test POST /password-reset/reset with weak password"""
        request_data = {
            "email": "test@example.com",
            "password": "weak"
        }
        
        response = client.post("/password-reset/reset", json=request_data)
        
        assert response.status_code == 422

    def test_reset_password_api_invalid_email_format(self, client):
        """Test POST /password-reset/reset with invalid email format"""
        request_data = {
            "email": "invalid-email",
            "password": "ValidPass123!"
        }
        
        response = client.post("/password-reset/reset", json=request_data)
        
        assert response.status_code == 422

    def test_reset_password_api_missing_email(self, client):
        """Test POST /password-reset/reset without email"""
        request_data = {
            "password": "ValidPass123!"
        }
        
        response = client.post("/password-reset/reset", json=request_data)
        
        assert response.status_code == 422

    def test_reset_password_api_missing_password(self, client):
        """Test POST /password-reset/reset without password"""
        request_data = {
            "email": "test@example.com"
        }
        
        response = client.post("/password-reset/reset", json=request_data)
        
        assert response.status_code == 422