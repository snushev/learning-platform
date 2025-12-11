from rest_framework import serializers
from .models import Enrollment, LessonProgress
from lessons.serializers import SimpleLessonSerializer
from users.serializers import UserProfileSerializer
from courses.serializers import SimpleCourseSerializer
from courses.models import Course


class EnrollmentSerializer(serializers.ModelSerializer):
    student = UserProfileSerializer(read_only=True)
    course = SimpleCourseSerializer(read_only=True)
    course_id = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all(), write_only=True, source="course")

    class Meta:
        model = Enrollment
        fields = [
            "id",
            "student",
            "course",
            "course_id",
            "enrolled_at",
            "progress_percentage",
            "is_completed",
            "completed_at",
        ]
        read_only_fields = ["id", "student", "enrolled_at", "progress_percentage", "is_completed", "comleted_at"]


class LessonProgressSerializer(serializers.ModelSerializer):
    lesson = SimpleLessonSerializer(read_only=True)

    class Meta:
        model = LessonProgress
        fields = ["lesson", "is_viewed", "completion_percentage", "completed_at"]
