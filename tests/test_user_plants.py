import pytest
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock
from fastapi import UploadFile, HTTPException
from io import BytesIO
from app.services.user_plant_service import (
    get_user_plant, get_user_plants_minimal, create_user_plant,
    delete_user_plant, record_watering, record_sunfilling
)
from app.schemas.user_plant import UserPlantBase

class TestUserPlantService:
    def test_get_user_plant_success(self, db_session, sample_user_plant, sample_user):
        """Test retrieving user plant by ID"""
        result = get_user_plant(db_session, sample_user_plant.id, sample_user.id)
        
        assert result is not None
        assert result.id == sample_user_plant.id
        assert result.name == "My Test Plant"
        assert hasattr(result, 'care_status')

    def test_get_user_plant_wrong_owner(self, db_session, sample_user_plant):
        """Test retrieving user plant with wrong owner ID"""
        result = get_user_plant(db_session, sample_user_plant.id, 999)
        
        assert result is None

    def test_create_user_plant_success(self, db_session, sample_user, sample_plant):
        """Test creating a new user plant"""
        now = datetime.utcnow()
        plant_data = UserPlantBase(
            plant_id=sample_plant.id,
            name="New Plant",
            last_watering=now,
            last_sunfilling=now,
            image="test.jpg",
            thumbnail="thumbnails/test_thumbnail.jpg"
        )
        
        result = create_user_plant(db_session, plant_data, sample_user.id)
        
        assert result.name == "New Plant"
        assert result.plant_id == sample_plant.id
        assert result.owner_id == sample_user.id

    def test_create_user_plant_invalid_plant_id(self, db_session, sample_user):
        """Test creating user plant with invalid plant ID"""
        now = datetime.utcnow()
        plant_data = UserPlantBase(
            plant_id=999,
            name="Invalid Plant",
            last_watering=now,
            last_sunfilling=now,
            image="test.jpg",
            thumbnail="thumbnails/test_thumbnail.jpg"
        )
        
        with pytest.raises(HTTPException):
            create_user_plant(db_session, plant_data, sample_user.id)

    def test_delete_user_plant_success(self, db_session, sample_user_plant, sample_user):
        """Test deleting user plant"""
        plant_id = sample_user_plant.id
        
        result = delete_user_plant(db_session, plant_id, sample_user.id)
        
        assert result is True
        deleted_plant = get_user_plant(db_session, plant_id, sample_user.id)
        assert deleted_plant is None

    def test_delete_user_plant_not_found(self, db_session, sample_user):
        """Test deleting non-existent user plant"""
        with pytest.raises(HTTPException):
            delete_user_plant(db_session, 999, sample_user.id)

    def test_record_watering(self, db_session, sample_user_plant, sample_user):
        """Test recording watering action"""
        old_watering = sample_user_plant.last_watering
        
        result = record_watering(db_session, sample_user_plant.id, sample_user.id)
        
        assert result.last_watering > old_watering

    def test_record_sunfilling(self, db_session, sample_user_plant, sample_user):
        """Test recording sunfilling action"""
        old_sunfilling = sample_user_plant.last_sunfilling
        
        result = record_sunfilling(db_session, sample_user_plant.id, sample_user.id)
        
        assert result.last_sunfilling > old_sunfilling

class TestUserPlantAPI:
    def test_get_single_user_plant(self, client, db_session, sample_user, sample_user_plant):
        """Test GET /user-plants/{id} endpoint"""
        from app.utils.security import create_access_token
        token = create_access_token(data={"sub": sample_user.username})
        headers = {"Authorization": f"Bearer {token}"}
        
        response = client.get(f"/user-plants/{sample_user_plant.id}", headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "My Test Plant"
        assert data["id"] == sample_user_plant.id

    def test_get_single_user_plant_not_found(self, client, db_session, sample_user):
        """Test GET /user-plants/{id} with non-existent plant"""
        from app.utils.security import create_access_token
        token = create_access_token(data={"sub": sample_user.username})
        headers = {"Authorization": f"Bearer {token}"}
        
        response = client.get("/user-plants/999", headers=headers)
        
        assert response.status_code == 404

    def test_water_plant(self, client, db_session, sample_user, sample_user_plant):
        """Test POST /user-plants/{id}/water endpoint"""
        from app.utils.security import create_access_token
        token = create_access_token(data={"sub": sample_user.username})
        headers = {"Authorization": f"Bearer {token}"}
        
        response = client.post(f"/user-plants/{sample_user_plant.id}/water", headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        assert "last_watering" in data

    def test_sunfill_plant(self, client, db_session, sample_user, sample_user_plant):
        """Test POST /user-plants/{id}/sunfill endpoint"""
        from app.utils.security import create_access_token
        token = create_access_token(data={"sub": sample_user.username})
        headers = {"Authorization": f"Bearer {token}"}
        
        response = client.post(f"/user-plants/{sample_user_plant.id}/sunfill", headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        assert "last_sunfilling" in data

    def test_remove_user_plant(self, client, db_session, sample_user, sample_user_plant):
        """Test DELETE /user-plants/{id} endpoint"""
        from app.utils.security import create_access_token
        token = create_access_token(data={"sub": sample_user.username})
        headers = {"Authorization": f"Bearer {token}"}
        
        response = client.delete(f"/user-plants/{sample_user_plant.id}", headers=headers)
        
        assert response.status_code == 200

    @patch('app.utils.image_handler.save_image')
    def test_create_user_plant_with_form(self, mock_save_image, client, db_session, sample_user, sample_plant):
        """Test POST /user-plants/create-with-form endpoint"""
        mock_save_image.return_value = {
            "filename": "test_image.jpg",
            "thumbnail": "thumbnails/test_image_thumbnail.jpg"
        }
        
        from app.utils.security import create_access_token
        token = create_access_token(data={"sub": sample_user.username})
        headers = {"Authorization": f"Bearer {token}"}
        
        form_data = {
            "plant_id": sample_plant.id,
            "name": "Form Plant"
        }
        
        files = {"file": ("test.jpg", BytesIO(b"fake image content"), "image/jpeg")}
        
        response = client.post(
            "/user-plants/create-with-form",
            data=form_data,
            files=files,
            headers=headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Form Plant"
        assert data["plant_id"] == sample_plant.id

    def test_create_user_plant_without_file(self, client, db_session, sample_user, sample_plant):
        """Test creating plant without file upload"""
        from app.utils.security import create_access_token
        token = create_access_token(data={"sub": sample_user.username})
        headers = {"Authorization": f"Bearer {token}"}
        
        form_data = {
            "plant_id": sample_plant.id,
            "name": "No File Plant"
        }
        
        response = client.post(
            "/user-plants/create-with-form",
            data=form_data,
            headers=headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "No File Plant"

    def test_unauthorized_access(self, client, sample_user_plant):
        """Test accessing endpoints without authentication"""
        response = client.get("/user-plants/")
        assert response.status_code == 401
        
        response = client.get(f"/user-plants/{sample_user_plant.id}")
        assert response.status_code == 401
        
        response = client.post(f"/user-plants/{sample_user_plant.id}/water")
        assert response.status_code == 401

    def test_invalid_token(self, client, sample_user_plant):
        """Test accessing endpoints with invalid token"""
        headers = {"Authorization": "Bearer invalid_token"}
        
        response = client.get("/user-plants/", headers=headers)
        assert response.status_code == 401
        
        response = client.get(f"/user-plants/{sample_user_plant.id}", headers=headers)
        assert response.status_code == 401

    def test_missing_authorization_header(self, client, sample_user_plant):
        """Test accessing endpoints without Authorization header"""
        headers = {"Some-Other-Header": "value"}
        
        response = client.get("/user-plants/", headers=headers)
        assert response.status_code == 401