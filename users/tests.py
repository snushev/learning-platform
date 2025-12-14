import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from users.models import User


@pytest.mark.django_db
class TestUserAuthentication:

    def setup_method(self):
        self.client = APIClient()

    def test_user_registration(self):
        """Test user can register successfully"""
        url = reverse("register")
        data = {"username": "testuser", "email": "test@example.com", "password": "testpass123", "role": "Student"}
        response = self.client.post(url, data, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert "access" in response.data
        assert "refresh" in response.data
        assert User.objects.filter(username="testuser").exists()

    def test_user_login(self):
        """Test user can login with correct credentials"""
        # Create user
        User.objects.create_user(username="testuser", email="test@example.com", password="testpass123", role="Student")

        url = reverse("login")
        data = {"login": "testuser", "password": "testpass123"}
        response = self.client.post(url, data, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert "access" in response.data

    def test_login_with_invalid_credentials(self):
        """Test login fails with wrong password"""
        User.objects.create_user(username="testuser", password="correctpass", role="Student")

        url = reverse("login")
        data = {"login": "testuser", "password": "wrongpass"}
        response = self.client.post(url, data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
