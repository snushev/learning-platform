import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from users.models import User
from courses.models import Course, Category


@pytest.mark.django_db
class TestCourses:

    def setup_method(self):
        self.client = APIClient()

        # Create instructor
        self.instructor = User.objects.create_user(
            username="instructor", password="pass123", email="instructor@courses.com", role="Instructor"
        )

        # Create student
        self.student = User.objects.create_user(
            username="student", password="pass123", email="student@courses.com", role="Student"
        )

        # Create category
        self.category = Category.objects.create(name="Programming", description="Programming courses")



    def test_instructor_can_create_course(self):
        """Test instructor can create a course"""
        self.client.force_authenticate(user=self.instructor)

        url = reverse("courses-list")
        data = {
            "title": "New Course",
            "description": "Course description",
            "category_id": self.category.id,
            "level": "beginner",
            "price": 99.99,
        }
        response = self.client.post(url, data, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert Course.objects.filter(title="New Course").exists()

    def test_list_courses(self):
        """Test anyone can list courses"""
        Course.objects.create(
            title="Test Course",
            instructor=self.instructor,
            category=self.category,
            level="beginner",
            is_published=True,
        )

        url = reverse("courses-list")
        response = self.client.get(url)

        assert response.status_code == status.HTTP_200_OK

        assert len(response.data["results"]) == 1

        assert response.data["count"] == 1
