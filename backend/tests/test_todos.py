import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

class TestTodos:
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup test user and get auth token"""
        # Register test user
        response = client.post(
            "/api/auth/register",
            json={
                "email": "todotest@example.com",
                "username": "todouser",
                "password": "TestPassword123!"
            }
        )
        self.token = response.json()["access_token"]
        self.headers = {"Authorization": f"Bearer {self.token}"}

    def test_create_todo(self):
        """Test creating a new todo"""
        response = client.post(
            "/api/todos",
            json={
                "title": "Test Todo",
                "description": "Test description",
                "priority": "medium",
                "status": "pending"
            },
            headers=self.headers
        )
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Test Todo"
        assert data["description"] == "Test description"
        assert data["priority"] == "medium"
        assert data["status"] == "pending"

    def test_get_todos(self):
        """Test getting todos list"""
        # Create a todo first
        client.post(
            "/api/todos",
            json={
                "title": "Get Test Todo",
                "description": "Test description"
            },
            headers=self.headers
        )
        
        # Get todos
        response = client.get("/api/todos", headers=self.headers)
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert len(data["items"]) >= 1
        assert data["total"] >= 1

    def test_get_todo_by_id(self):
        """Test getting a specific todo by ID"""
        # Create a todo first
        create_response = client.post(
            "/api/todos",
            json={
                "title": "Specific Todo",
                "description": "Specific description"
            },
            headers=self.headers
        )
        todo_id = create_response.json()["id"]
        
        # Get specific todo
        response = client.get(f"/api/todos/{todo_id}", headers=self.headers)
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == todo_id
        assert data["title"] == "Specific Todo"

    def test_update_todo(self):
        """Test updating a todo"""
        # Create a todo first
        create_response = client.post(
            "/api/todos",
            json={
                "title": "Update Todo",
                "description": "Original description"
            },
            headers=self.headers
        )
        todo_id = create_response.json()["id"]
        
        # Update todo
        response = client.put(
            f"/api/todos/{todo_id}",
            json={
                "title": "Updated Todo",
                "description": "Updated description",
                "priority": "high"
            },
            headers=self.headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated Todo"
        assert data["description"] == "Updated description"
        assert data["priority"] == "high"

    def test_delete_todo(self):
        """Test deleting a todo"""
        # Create a todo first
        create_response = client.post(
            "/api/todos",
            json={
                "title": "Delete Todo",
                "description": "To be deleted"
            },
            headers=self.headers
        )
        todo_id = create_response.json()["id"]
        
        # Delete todo
        response = client.delete(f"/api/todos/{todo_id}", headers=self.headers)
        assert response.status_code == 204
        
        # Verify deletion
        get_response = client.get(f"/api/todos/{todo_id}", headers=self.headers)
        assert get_response.status_code == 404

    def test_toggle_todo_status(self):
        """Test toggling todo status"""
        # Create a todo first
        create_response = client.post(
            "/api/todos",
            json={
                "title": "Toggle Todo",
                "status": "pending"
            },
            headers=self.headers
        )
        todo_id = create_response.json()["id"]
        
        # Toggle status
        response = client.patch(f"/api/todos/{todo_id}/toggle", headers=self.headers)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "completed"

    def test_search_todos(self):
        """Test searching todos"""
        # Create todos with different titles
        client.post(
            "/api/todos",
            json={"title": "Important task"},
            headers=self.headers
        )
        client.post(
            "/api/todos",
            json={"title": "Regular work"},
            headers=self.headers
        )
        
        # Search for "important"
        response = client.get(
            "/api/todos?search=important",
            headers=self.headers
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) >= 1
        assert "important" in data["items"][0]["title"].lower()

    def test_filter_todos_by_status(self):
        """Test filtering todos by status"""
        # Create todos with different statuses
        client.post(
            "/api/todos",
            json={"title": "Pending task", "status": "pending"},
            headers=self.headers
        )
        create_response = client.post(
            "/api/todos",
            json={"title": "Completed task", "status": "pending"},
            headers=self.headers
        )
        
        # Toggle one to completed
        todo_id = create_response.json()["id"]
        client.patch(f"/api/todos/{todo_id}/toggle", headers=self.headers)
        
        # Filter by completed
        response = client.get(
            "/api/todos?status=completed",
            headers=self.headers
        )
        assert response.status_code == 200
        data = response.json()
        for todo in data["items"]:
            assert todo["status"] == "completed"

    def test_unauthorized_access(self):
        """Test accessing todos without authentication"""
        response = client.get("/api/todos")
        assert response.status_code == 401

    def test_access_other_user_todo(self):
        """Test accessing todo from another user"""
        # Create another user
        client.post(
            "/api/auth/register",
            json={
                "email": "other@example.com",
                "username": "otheruser",
                "password": "TestPassword123!"
            }
        )
        
        # Create todo with first user
        create_response = client.post(
            "/api/todos",
            json={"title": "Private todo"},
            headers=self.headers
        )
        todo_id = create_response.json()["id"]
        
        # Try to access with second user
        login_response = client.post(
            "/api/auth/login",
            json={
                "email": "other@example.com",
                "password": "TestPassword123!"
            }
        )
        other_token = login_response.json()["access_token"]
        other_headers = {"Authorization": f"Bearer {other_token}"}
        
        response = client.get(f"/api/todos/{todo_id}", headers=other_headers)
        assert response.status_code == 404