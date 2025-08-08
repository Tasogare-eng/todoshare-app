import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

class TestCategories:
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup test user and get auth token"""
        # Register test user
        response = client.post(
            "/api/auth/register",
            json={
                "email": "categorytest@example.com",
                "username": "categoryuser",
                "password": "TestPassword123!"
            }
        )
        self.token = response.json()["access_token"]
        self.headers = {"Authorization": f"Bearer {self.token}"}

    def test_get_default_categories(self):
        """Test getting default categories for new user"""
        response = client.get("/api/categories", headers=self.headers)
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 4  # Default categories
        
        # Check for default category names
        category_names = [cat["name"] for cat in data["items"]]
        assert "仕事" in category_names
        assert "プライベート" in category_names
        assert "買い物" in category_names
        assert "その他" in category_names

    def test_create_category(self):
        """Test creating a new category"""
        response = client.post(
            "/api/categories",
            json={
                "name": "テストカテゴリ",
                "color": "#ff0000",
                "description": "テスト用カテゴリです"
            },
            headers=self.headers
        )
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "テストカテゴリ"
        assert data["color"] == "#ff0000"
        assert data["description"] == "テスト用カテゴリです"

    def test_create_duplicate_category(self):
        """Test creating category with duplicate name"""
        # Create first category
        client.post(
            "/api/categories",
            json={
                "name": "重複テスト",
                "color": "#00ff00"
            },
            headers=self.headers
        )
        
        # Try to create duplicate
        response = client.post(
            "/api/categories",
            json={
                "name": "重複テスト",
                "color": "#0000ff"
            },
            headers=self.headers
        )
        assert response.status_code == 400

    def test_get_category_by_id(self):
        """Test getting a specific category by ID"""
        # Create category first
        create_response = client.post(
            "/api/categories",
            json={
                "name": "IDテスト",
                "color": "#123456"
            },
            headers=self.headers
        )
        category_id = create_response.json()["id"]
        
        # Get specific category
        response = client.get(f"/api/categories/{category_id}", headers=self.headers)
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == category_id
        assert data["name"] == "IDテスト"

    def test_update_category(self):
        """Test updating a category"""
        # Create category first
        create_response = client.post(
            "/api/categories",
            json={
                "name": "更新前",
                "color": "#111111"
            },
            headers=self.headers
        )
        category_id = create_response.json()["id"]
        
        # Update category
        response = client.put(
            f"/api/categories/{category_id}",
            json={
                "name": "更新後",
                "color": "#222222",
                "description": "更新されました"
            },
            headers=self.headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "更新後"
        assert data["color"] == "#222222"
        assert data["description"] == "更新されました"

    def test_delete_category(self):
        """Test deleting a category"""
        # Create category first
        create_response = client.post(
            "/api/categories",
            json={
                "name": "削除テスト",
                "color": "#999999"
            },
            headers=self.headers
        )
        category_id = create_response.json()["id"]
        
        # Delete category
        response = client.delete(f"/api/categories/{category_id}", headers=self.headers)
        assert response.status_code == 204
        
        # Verify deletion
        get_response = client.get(f"/api/categories/{category_id}", headers=self.headers)
        assert get_response.status_code == 404

    def test_invalid_color_format(self):
        """Test creating category with invalid color format"""
        response = client.post(
            "/api/categories",
            json={
                "name": "Invalid Color",
                "color": "not-a-color"
            },
            headers=self.headers
        )
        assert response.status_code == 422

    def test_category_name_length_validation(self):
        """Test category name length validation"""
        # Too long name (over 30 characters)
        response = client.post(
            "/api/categories",
            json={
                "name": "a" * 31,
                "color": "#000000"
            },
            headers=self.headers
        )
        assert response.status_code == 422

    def test_unauthorized_category_access(self):
        """Test accessing categories without authentication"""
        response = client.get("/api/categories")
        assert response.status_code == 401

    def test_access_other_user_category(self):
        """Test accessing category from another user"""
        # Create category with first user
        create_response = client.post(
            "/api/categories",
            json={
                "name": "Private Category",
                "color": "#private"
            },
            headers=self.headers
        )
        category_id = create_response.json()["id"]
        
        # Create another user
        client.post(
            "/api/auth/register",
            json={
                "email": "othercategory@example.com",
                "username": "othercategoryuser",
                "password": "TestPassword123!"
            }
        )
        
        # Login as second user
        login_response = client.post(
            "/api/auth/login",
            json={
                "email": "othercategory@example.com",
                "password": "TestPassword123!"
            }
        )
        other_token = login_response.json()["access_token"]
        other_headers = {"Authorization": f"Bearer {other_token}"}
        
        # Try to access first user's category
        response = client.get(f"/api/categories/{category_id}", headers=other_headers)
        assert response.status_code == 404