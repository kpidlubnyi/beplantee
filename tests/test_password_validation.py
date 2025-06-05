import pytest
from app.utils.password_validator import validate_password

class TestPasswordValidator:
    def test_valid_password(self):
        """Test password that meets all requirements"""
        password = "ValidPass123!"
        result = validate_password(password)
        
        assert result["valid"] is True
        assert len(result["errors"]) == 0

    def test_password_too_short(self):
        """Test password shorter than 8 characters"""
        password = "Short1!"
        result = validate_password(password)
        
        assert result["valid"] is False
        assert "Password must be at least 8 characters long" in result["errors"]

    def test_password_no_uppercase(self):
        """Test password without uppercase letters"""
        password = "lowercase123!"
        result = validate_password(password)
        
        assert result["valid"] is False
        assert "Password must contain at least one uppercase letter" in result["errors"]

    def test_password_no_lowercase(self):
        """Test password without lowercase letters"""
        password = "UPPERCASE123!"
        result = validate_password(password)
        
        assert result["valid"] is False
        assert "Password must contain at least one lowercase letter" in result["errors"]

    def test_password_no_digit(self):
        """Test password without digits"""
        password = "NoDigits!"
        result = validate_password(password)
        
        assert result["valid"] is False
        assert "Password must contain at least one digit" in result["errors"]

    def test_password_no_special_char(self):
        """Test password without special characters"""
        password = "NoSpecial123"
        result = validate_password(password)
        
        assert result["valid"] is False
        assert "Password must contain at least one special character" in result["errors"]

    def test_password_invalid_characters(self):
        """Test password with invalid characters"""
        password = "ValidPass123!ąć"
        result = validate_password(password)
        
        assert result["valid"] is False
        assert "Password must contain only Latin letters, digits, and special characters" in result["errors"]

    def test_password_multiple_errors(self):
        """Test password with multiple validation errors"""
        password = "abc"
        result = validate_password(password)
        
        assert result["valid"] is False
        assert len(result["errors"]) >= 4

    def test_password_edge_case_length(self):
        """Test password with exactly 8 characters"""
        password = "Valid12!"
        result = validate_password(password)
        
        assert result["valid"] is True
        assert len(result["errors"]) == 0

    def test_password_all_special_chars(self):
        """Test password with various special characters"""
        special_chars = "!@#$%^&*()_+-=[]{};\':\"\\|,.<>/?"
        for char in special_chars:
            password = f"ValidP1{char}"
            result = validate_password(password)
            assert result["valid"] is True, f"Failed for special character: {char}"

class TestPasswordValidationAPI:
    def test_validate_password_api_valid(self, client):
        """Test password validation API with valid password"""
        response = client.post("/password-validation/", json="ValidPass123!")
        
        assert response.status_code == 200
        data = response.json()
        assert data["errors"] == []

    def test_validate_password_api_invalid(self, client):
        """Test password validation API with invalid password"""
        response = client.post("/password-validation/", json="weak")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data["errors"]) > 0