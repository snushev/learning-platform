from rest_framework import serializers
from courses.serializers import CourseSerializer
from courses.models import Course
from .models import Lesson

class LessonSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)
    course_id = serializers.PrimaryKeyRelatedField(
    queryset=Course.objects.all(),
    write_only=True,
    source='course'
)

    class Meta:
        model = Lesson
        fields = '__all__'
        read_only_fields = ['course', 'id', 'created_at','updated_at']

class SimpleLessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'order']
    