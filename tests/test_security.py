import pytest
from datetime import datetime, timedelta
from unittest.mock import patch
from jose import jwt
from fastapi import HTTPException
from app.utils.security import (
    verify_password, get_password_hash, create_access_token, get_current_user
)
from app.config import settings
import time

class TestSecurityUtils:
    def test_password_hashing_and_verification(self):
        """Test password hashing and verification"""
        password = "TestPassword123!"
        hashed = get_password_hash(password)
        
        assert hashed != password
        assert verify_password(password, hashed) is True
        assert verify_password("WrongPassword", hashed) is False

    def test_password_hash_uniqueness(self):
        """Test that same password produces different hashes"""
        password = "SamePassword123!"
        hash1 = get_password_hash(password)
        hash2 = get_password_hash(password)
        
        assert hash1 != hash2
        assert verify_password(password, hash1) is True
        assert verify_password(password, hash2) is True

    def test_create_access_token_default_expiry(self):
        """Test creating access token with default expiry"""
        data = {"sub": "testuser"}
        token = create_access_token(data)
        
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        assert payload["sub"] == "testuser"
        assert "exp" in payload
        
        exp_time = datetime.utcfromtimestamp(payload["exp"])
        expected_exp = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        time_diff = abs((exp_time - expected_exp).total_seconds())
        assert time_diff < 120 

    def test_create_access_token_custom_expiry(self):
        """Test creating access token with custom expiry"""
        data = {"sub": "testuser"}
        custom_delta = timedelta(hours=2)
        token = create_access_token(data, custom_delta)
        
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        exp_time = datetime.utcfromtimestamp(payload["exp"])
        expected_exp = datetime.utcnow() + custom_delta
        time_diff = abs((exp_time - expected_exp).total_seconds())
        assert time_diff < 120  

    def test_create_access_token_additional_data(self):
        """Test creating access token with additional data"""
        data = {"sub": "testuser", "role": "admin", "permissions": ["read", "write"]}
        token = create_access_token(data)
        
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        assert payload["sub"] == "testuser"
        assert payload["role"] == "admin"
        assert payload["permissions"] == ["read", "write"]

    def test_get_current_user_success(self, db_session, sample_user):
        """Test successful user retrieval from token"""
        token = create_access_token(data={"sub": sample_user.username})
        
        result = get_current_user(db_session, token)
        
        assert result.id == sample_user.id
        assert result.username == sample_user.username

    def test_get_current_user_invalid_token(self, db_session):
        """Test user retrieval with invalid token"""
        invalid_token = "invalid.token.here"
        
        with pytest.raises(HTTPException) as exc_info:
            get_current_user(db_session, invalid_token)
        
        assert exc_info.value.status_code == 401
        assert "Could not validate credentials" in str(exc_info.value.detail)

    def test_get_current_user_expired_token(self, db_session, sample_user):
        """Test user retrieval with expired token"""
        past_time = datetime.utcnow() - timedelta(hours=1)
        expired_payload = {
            "sub": sample_user.username,
            "exp": past_time.timestamp()
        }
        expired_token = jwt.encode(expired_payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        
        with pytest.raises(HTTPException) as exc_info:
            get_current_user(db_session, expired_token)
        
        assert exc_info.value.status_code == 401

    def test_get_current_user_no_subject(self, db_session):
        """Test user retrieval with token missing subject"""
        payload = {"exp": (datetime.utcnow() + timedelta(hours=1)).timestamp()}
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        
        with pytest.raises(HTTPException) as exc_info:
            get_current_user(db_session, token)
        
        assert exc_info.value.status_code == 401

    def test_get_current_user_nonexistent_user(self, db_session):
        """Test user retrieval with token for non-existent user"""
        token = create_access_token(data={"sub": "nonexistent_user"})
        
        with pytest.raises(HTTPException) as exc_info:
            get_current_user(db_session, token)
        
        assert exc_info.value.status_code == 401

    def test_get_current_user_wrong_algorithm(self, db_session, sample_user):
        """Test user retrieval with token signed with wrong algorithm"""
        payload = {
            "sub": sample_user.username,
            "exp": (datetime.utcnow() + timedelta(hours=1)).timestamp()
        }
        wrong_token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS512")
        
        with pytest.raises(HTTPException) as exc_info:
            get_current_user(db_session, wrong_token)
        
        assert exc_info.value.status_code == 401

    def test_get_current_user_wrong_secret(self, db_session, sample_user):
        """Test user retrieval with token signed with wrong secret"""
        payload = {
            "sub": sample_user.username,
            "exp": (datetime.utcnow() + timedelta(hours=1)).timestamp()
        }
        wrong_token = jwt.encode(payload, "wrong_secret", algorithm=settings.ALGORITHM)
        
        with pytest.raises(HTTPException) as exc_info:
            get_current_user(db_session, wrong_token)
        
        assert exc_info.value.status_code == 401

class TestSecurityIntegration:
    def test_password_change_flow(self, db_session, sample_user):
        """Test complete password change flow"""
        old_hash = sample_user.hashed_password
        new_password = "NewSecurePass123!"
        
        new_hash = get_password_hash(new_password)
        sample_user.hashed_password = new_hash
        db_session.commit()
        
        assert verify_password(new_password, new_hash) is True
        assert verify_password("testpassword123", new_hash) is False
        assert new_hash != old_hash

    def test_token_refresh_simulation(self, db_session, sample_user):
        """Test token refresh simulation with guaranteed different tokens"""
        old_token = create_access_token(data={"sub": sample_user.username})
        
        user_from_old_token = get_current_user(db_session, old_token)
        assert user_from_old_token.id == sample_user.id
        
        time.sleep(0.1)
        
        new_token = create_access_token(
            data={"sub": user_from_old_token.username},
            expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES + 1)
        )
        user_from_new_token = get_current_user(db_session, new_token)
        assert user_from_new_token.id == sample_user.id
        
        assert old_token != new_token

    def test_token_payload_integrity(self, sample_user):
        """Test that token payload remains intact"""
        original_data = {
            "sub": sample_user.username,
            "user_id": sample_user.id,
            "role": "user"
        }
        
        token = create_access_token(data=original_data)
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        
        assert payload["sub"] == original_data["sub"]
        assert payload["user_id"] == original_data["user_id"]
        assert payload["role"] == original_data["role"]
        assert "exp" in payload