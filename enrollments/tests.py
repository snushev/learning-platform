import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from users.models import User
from courses.models import Course, Category
from enrollments.models import Enrollment


@pytest.mark.django_db
class TestEnrollments:

    def setup_method(self):
        self.client = APIClient()

        self.instructor = User.objects.create_user(
            username="instructor", password="pass123", email="instructor@enroll.com", role="Instructor"
        )

        self.student = User.objects.create_user(
            username="student", password="pass123", email="student@enroll.com", role="Student"
        )

        category = Category.objects.create(name="Programming")

        self.course = Course.objects.create(
            title="Test Course", instructor=self.instructor, category=category, level="beginner", is_published=True
        )

    def test_cannot_enroll_twice(self):
        """Test student cannot enroll in same course twice"""
        self.client.force_authenticate(user=self.student)

        # First enrollment
        Enrollment.objects.create(student=self.student, course=self.course)

        # Try to enroll again
        url = reverse("enrollments-list")
        data = {"course_id": self.course.id}
        response = self.client.post(url, data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
