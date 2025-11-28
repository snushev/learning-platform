from rest_framework import serializers
from .models import Category, Course
from users.serializers import UserProfileSerializer


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "description"]


class CourseSerializer(serializers.ModelSerializer):
    instructor = UserProfileSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), write_only=True, source="category"
    )

    class Meta:
        model = Course
        fields = [
            "id",
            "title",
            "description",
            "instructor",
            "category",
            "category_id",
            "level",
            "price",
            "image",
            "is_published",
            "enrollment_count",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "instructor", "enrollment_count", "created_at", "updated_at"]
