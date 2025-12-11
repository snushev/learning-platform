from rest_framework import serializers
from .models import CourseRating
from courses.models import Course
from users.serializers import BasicUserSerializer

class CourseRatingSerializer(serializers.ModelSerializer):
    course_id = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all(), write_only=True, source="course")
    student =  BasicUserSerializer(read_only=True)

    class Meta:
        model = CourseRating
        fields = ['id', 'student', 'course', 'course_id', 'rating', 'review_text', 'created_at', 'updated_at']
        read_only_fields = ['id', 'student', 'created_at', 'updated_at']
