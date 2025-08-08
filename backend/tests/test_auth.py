import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

class TestAuth:
    def test_register_user(self):
        """Test user registration"""
        response = client.post(
            "/api/auth/register",
            json={
                "email": "test@example.com",
                "username": "testuser",
                "password": "TestPassword123!"
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == "test@example.com"
        assert data["username"] == "testuser"
        assert "access_token" in data

    def test_register_duplicate_user(self):
        """Test registration with duplicate email"""
        # First registration
        client.post(
            "/api/auth/register",
            json={
                "email": "duplicate@example.com",
                "username": "user1",
                "password": "TestPassword123!"
            }
        )
        
        # Second registration with same email
        response = client.post(
            "/api/auth/register",
            json={
                "email": "duplicate@example.com",
                "username": "user2",
                "password": "TestPassword123!"
            }
        )
        assert response.status_code == 400

    def test_login_user(self):
        """Test user login"""
        # Register a user first
        client.post(
            "/api/auth/register",
            json={
                "email": "login@example.com",
                "username": "loginuser",
                "password": "TestPassword123!"
            }
        )
        
        # Login
        response = client.post(
            "/api/auth/login",
            json={
                "email": "login@example.com",
                "password": "TestPassword123!"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["user"]["email"] == "login@example.com"

    def test_login_invalid_credentials(self):
        """Test login with invalid credentials"""
        response = client.post(
            "/api/auth/login",
            json={
                "email": "nonexistent@example.com",
                "password": "WrongPassword"
            }
        )
        assert response.status_code == 400

    def test_weak_password(self):
        """Test registration with weak password"""
        response = client.post(
            "/api/auth/register",
            json={
                "email": "weak@example.com",
                "username": "weakuser",
                "password": "123"
            }
        )
        assert response.status_code == 400

    def test_protected_route_without_token(self):
        """Test accessing protected route without token"""
        response = client.get("/api/auth/me")
        assert response.status_code == 401

    def test_protected_route_with_token(self):
        """Test accessing protected route with valid token"""
        # Register and get token
        register_response = client.post(
            "/api/auth/register",
            json={
                "email": "protected@example.com",
                "username": "protecteduser",
                "password": "TestPassword123!"
            }
        )
        token = register_response.json()["access_token"]
        
        # Access protected route
        response = client.get(
            "/api/auth/me",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "protected@example.com"