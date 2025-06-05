import pytest

class TestFAQAPI:
    def test_get_faq_structure(self, client):
        """Test FAQ endpoint returns proper structure"""
        response = client.get("/faq")
        
        assert response.status_code == 200
        data = response.json()
        
        assert "categories" in data
        assert isinstance(data["categories"], list)
        assert len(data["categories"]) > 0

    def test_faq_categories_structure(self, client):
        """Test FAQ categories have required fields"""
        response = client.get("/faq")
        data = response.json()
        
        for category in data["categories"]:
            assert "title" in category
            assert "items" in category
            assert isinstance(category["title"], str)
            assert isinstance(category["items"], list)
            assert len(category["title"]) > 0

    def test_faq_items_structure(self, client):
        """Test FAQ items have required fields"""
        response = client.get("/faq")
        data = response.json()
        
        for category in data["categories"]:
            for item in category["items"]:
                assert "question" in item
                assert "answer" in item
                assert isinstance(item["question"], str)
                assert isinstance(item["answer"], str)
                assert len(item["question"]) > 0
                assert len(item["answer"]) > 0

    def test_faq_content_categories(self, client):
        """Test FAQ contains expected categories"""
        response = client.get("/faq")
        data = response.json()
        
        category_titles = [cat["title"] for cat in data["categories"]]
        
        expected_categories = [
            "General Questions",
            "Account Management", 
            "Plant Management",
            "Troubleshooting",
            "Technical Questions",
            "Privacy & Security",
            "Contact & Support"
        ]
        
        for expected in expected_categories:
            assert expected in category_titles

    def test_faq_has_beplantee_content(self, client):
        """Test FAQ contains BePlantee specific content"""
        response = client.get("/faq")
        data = response.json()
        
        all_content = str(data).lower()
        
        assert "beplantee" in all_content
        assert "plant" in all_content
        assert "watering" in all_content
        assert "sunlight" in all_content

    def test_faq_no_empty_categories(self, client):
        """Test that all FAQ categories have items"""
        response = client.get("/faq")
        data = response.json()
        
        for category in data["categories"]:
            assert len(category["items"]) > 0