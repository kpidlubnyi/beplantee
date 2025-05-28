import pytest
import os
import tempfile
from unittest.mock import patch, MagicMock, AsyncMock
from fastapi import UploadFile, HTTPException
from io import BytesIO
from PIL import Image
from app.utils.image_handler import (
    validate_image, optimize_image, save_image, delete_image, get_default_image_path
)

class TestImageHandler:
    def test_validate_image_valid_jpeg(self):
        """Test validation of valid JPEG image"""
        mock_file = MagicMock()
        mock_file.content_type = "image/jpeg"
        
        result = validate_image(mock_file)
        assert result is True

    def test_validate_image_valid_png(self):
        """Test validation of valid PNG image"""
        mock_file = MagicMock()
        mock_file.content_type = "image/png"
        
        result = validate_image(mock_file)
        assert result is True

    def test_validate_image_valid_gif(self):
        """Test validation of valid GIF image"""
        mock_file = MagicMock()
        mock_file.content_type = "image/gif"
        
        result = validate_image(mock_file)
        assert result is True

    def test_validate_image_invalid_type(self):
        """Test validation of invalid file type"""
        mock_file = MagicMock()
        mock_file.content_type = "text/plain"
        
        result = validate_image(mock_file)
        assert result is False

    def test_validate_image_invalid_video(self):
        """Test validation of video file"""
        mock_file = MagicMock()
        mock_file.content_type = "video/mp4"
        
        result = validate_image(mock_file)
        assert result is False

    @pytest.mark.asyncio
    async def test_optimize_image_jpeg(self):
        """Test image optimization for JPEG"""
        img = Image.new('RGB', (2000, 2000), color='red')
        img_bytes = BytesIO()
        img.save(img_bytes, format='JPEG')
        img_content = img_bytes.getvalue()
        
        result = await optimize_image(img_content, "test.jpg")
        
        assert result is not None
        optimized, thumbnail = result
        assert optimized[0] == "test.jpg"
        assert thumbnail[0] == "test_thumbnail.jpg"
        assert len(optimized[1]) > 0
        assert len(thumbnail[1]) > 0

    @pytest.mark.asyncio
    async def test_optimize_image_png(self):
        """Test image optimization for PNG"""
        img = Image.new('RGBA', (1500, 1500), color='blue')
        img_bytes = BytesIO()
        img.save(img_bytes, format='PNG')
        img_content = img_bytes.getvalue()
        
        result = await optimize_image(img_content, "test.png")
        
        assert result is not None
        optimized, thumbnail = result
        assert optimized[0] == "test.png"
        assert thumbnail[0] == "test_thumbnail.png"

    @pytest.mark.asyncio
    async def test_optimize_image_invalid_content(self):
        """Test image optimization with invalid content"""
        invalid_content = b"not an image"
        
        result = await optimize_image(invalid_content, "test.jpg")
        
        assert result == (None, None)

    @pytest.mark.asyncio
    @patch('app.utils.image_handler.settings')
    @patch('os.makedirs')
    @patch('builtins.open')
    async def test_save_image_success(self, mock_open, mock_makedirs, mock_settings):
        """Test successful image saving"""
        mock_settings.UPLOAD_DIRECTORY = "/tmp/uploads"
        
        img = Image.new('RGB', (500, 500), color='green')
        img_bytes = BytesIO()
        img.save(img_bytes, format='JPEG')
        
        mock_file = MagicMock(spec=UploadFile)
        mock_file.content_type = "image/jpeg"
        mock_file.filename = "test.jpg"
        mock_file.seek = AsyncMock()
        mock_file.read = AsyncMock(return_value=img_bytes.getvalue())
        
        with patch('app.utils.image_handler.optimize_image') as mock_optimize:
            mock_optimize.return_value = (
                ("optimized.jpg", b"optimized_content"),
                ("thumbnail.jpg", b"thumbnail_content")
            )
            
            result = await save_image(mock_file)
            
            assert "filename" in result
            assert "thumbnail" in result
            assert result["filename"] == "optimized.jpg"

    @pytest.mark.asyncio
    async def test_save_image_invalid_type(self):
        """Test saving invalid file type"""
        mock_file = MagicMock(spec=UploadFile)
        mock_file.content_type = "text/plain"
        
        with pytest.raises(HTTPException) as exc_info:
            await save_image(mock_file)
        
        assert exc_info.value.status_code == 400
        assert "File must be a valid image" in str(exc_info.value.detail)

    @patch('os.path.exists')
    @patch('os.path.isfile')
    @patch('os.remove')
    @patch('app.utils.image_handler.settings')
    def test_delete_image_success(self, mock_settings, mock_remove, mock_isfile, mock_exists):
        """Test successful image deletion"""
        mock_settings.UPLOAD_DIRECTORY = "/tmp/uploads"
        mock_exists.return_value = True
        mock_isfile.return_value = True
        
        result = delete_image("test.jpg")
        
        assert result is True
        assert mock_remove.call_count == 2

    @patch('os.path.exists')
    def test_delete_image_not_found(self, mock_exists):
        """Test deletion of non-existent image"""
        mock_exists.return_value = False
        
        result = delete_image("nonexistent.jpg")
        
        assert result is True

    @patch('os.remove')
    @patch('os.path.exists')
    @patch('os.path.isfile')
    @patch('app.utils.image_handler.settings')
    def test_delete_image_error(self, mock_settings, mock_isfile, mock_exists, mock_remove):
        """Test image deletion with error"""
        mock_settings.UPLOAD_DIRECTORY = "/tmp/uploads"
        mock_exists.return_value = True
        mock_isfile.return_value = True
        mock_remove.side_effect = OSError("Permission denied")
        
        result = delete_image("test.jpg")
        
        assert result is False

    def test_get_default_image_path(self):
        """Test getting default image paths"""
        result = get_default_image_path()
        
        assert "filename" in result
        assert "thumbnail" in result
        assert result["filename"] == "default_plant.png"
        assert result["thumbnail"] == "thumbnails/default_plant_thumbnail.png"

class TestImageHandlerIntegration:
    @pytest.mark.asyncio
    async def test_save_and_delete_cycle(self, temp_upload_dir):
        """Test complete save and delete cycle"""
        with patch('app.utils.image_handler.settings') as mock_settings:
            mock_settings.UPLOAD_DIRECTORY = temp_upload_dir
            
            img = Image.new('RGB', (800, 600), color='purple')
            img_bytes = BytesIO()
            img.save(img_bytes, format='JPEG')
            
            mock_file = MagicMock(spec=UploadFile)
            mock_file.content_type = "image/jpeg"
            mock_file.filename = "integration_test.jpg"
            mock_file.seek = AsyncMock()
            mock_file.read = AsyncMock(return_value=img_bytes.getvalue())
            
            result = await save_image(mock_file)
            
            assert "filename" in result
            saved_filename = result["filename"]
            
            assert os.path.exists(os.path.join(temp_upload_dir, saved_filename))
            
            delete_result = delete_image(saved_filename)
            assert delete_result is True