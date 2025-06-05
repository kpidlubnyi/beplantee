import pytest
from datetime import datetime, timedelta
from app.utils.care_calculator import (
    calculate_days_since, get_watering_level, get_sunfilling_level,
    calculate_care_status, WATERING_INTERVALS, SUNLIGHT_THRESHOLD
)

class TestCareCalculator:
    def test_calculate_days_since_current(self):
        """Test calculating days since current time"""
        now = datetime.utcnow()
        result = calculate_days_since(now)
        
        assert 0 <= result <= 0.1

    def test_calculate_days_since_past(self):
        """Test calculating days since past date"""
        past_date = datetime.utcnow() - timedelta(days=5, hours=12)
        result = calculate_days_since(past_date)
        
        assert 5.4 <= result <= 5.6

    def test_calculate_days_since_one_day(self):
        """Test calculating days since exactly one day ago"""
        one_day_ago = datetime.utcnow() - timedelta(days=1)
        result = calculate_days_since(one_day_ago)
        
        assert 0.9 <= result <= 1.1

    def test_get_watering_level_just_watered(self):
        """Test watering level for recently watered plant"""
        days_ago = 0.5
        interval = 5
        result = get_watering_level(days_ago, interval)
        
        assert result == 1

    def test_get_watering_level_needs_water_soon(self):
        """Test watering level for plant that needs water soon"""
        days_ago = 2
        interval = 5
        result = get_watering_level(days_ago, interval)
        
        assert result == 2

    def test_get_watering_level_moderate_need(self):
        """Test watering level for moderate watering need"""
        days_ago = 3
        interval = 5
        result = get_watering_level(days_ago, interval)
        
        assert result == 3

    def test_get_watering_level_high_need(self):
        """Test watering level for high watering need"""
        days_ago = 4
        interval = 5
        result = get_watering_level(days_ago, interval)
        
        assert result == 4

    def test_get_watering_level_urgent(self):
        """Test watering level for urgent watering need"""
        days_ago = 6
        interval = 5
        result = get_watering_level(days_ago, interval)
        
        assert result == 5

    def test_get_watering_level_overdue(self):
        """Test watering level for overdue plant"""
        days_ago = 10
        interval = 5
        result = get_watering_level(days_ago, interval)
        
        assert result == 5

    def test_get_sunfilling_level_recent(self):
        """Test sunfilling level for recently exposed plant"""
        days_ago = 0.5
        result = get_sunfilling_level(days_ago)
        
        assert result == 1

    def test_get_sunfilling_level_at_threshold(self):
        """Test sunfilling level at threshold"""
        days_ago = SUNLIGHT_THRESHOLD
        result = get_sunfilling_level(days_ago)
        
        assert result == 1

    def test_get_sunfilling_level_overdue(self):
        """Test sunfilling level for overdue sunlight"""
        days_ago = 1.5
        result = get_sunfilling_level(days_ago)
        
        assert result == 5

    def test_calculate_care_status_frequent_watering(self):
        """Test care status calculation for frequent watering plant"""
        now = datetime.utcnow()
        last_watering = now - timedelta(days=1)
        last_sunfilling = now - timedelta(hours=12)
        
        result = calculate_care_status(last_watering, last_sunfilling, "Frequent")
        
        assert result["watering_level"] == 3
        assert result["watering_interval"] == WATERING_INTERVALS["Frequent"]
        assert result["sunfilling_level"] == 1
        assert result["watering_days_ago"] == 1.0
        assert result["sunfilling_days_ago"] == 0.5

    def test_calculate_care_status_minimum_watering(self):
        """Test care status calculation for minimum watering plant"""
        now = datetime.utcnow()
        last_watering = now - timedelta(days=5)
        last_sunfilling = now - timedelta(hours=6)
        
        result = calculate_care_status(last_watering, last_sunfilling, "Minimum")
        
        assert result["watering_level"] == 3
        assert result["watering_interval"] == WATERING_INTERVALS["Minimum"]
        assert result["sunfilling_level"] == 1

    def test_calculate_care_status_unknown_watering_type(self):
        """Test care status calculation with unknown watering type"""
        now = datetime.utcnow()
        last_watering = now - timedelta(days=3)
        last_sunfilling = now - timedelta(hours=12)
        
        result = calculate_care_status(last_watering, last_sunfilling, "Unknown")
        
        assert result["watering_interval"] == 7

    def test_watering_level_edge_cases(self):
        """Test edge cases for watering level calculation"""
        assert get_watering_level(0, 5) == 1
        
        assert get_watering_level(1, 5) == 1
        
        assert get_watering_level(2, 5) == 2
        
        assert get_watering_level(3, 5) == 3
        
        assert get_watering_level(4, 5) == 4
        
        assert get_watering_level(5, 5) == 5
        assert get_watering_level(10, 5) == 5