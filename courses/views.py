from rest_framework import viewsets
from .models import Category, Course
from .serializers import CourseSerializer, CategorySerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from config.permissions import IsAdminOrReadOnly
from rest_framework.exceptions import PermissionDenied


class CategoryViewset(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]


class CourseViewset(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filterset_fields = ["category", "level"]
    search_fields = ["title", "description"]
    ordering_fields = ["created_at", "enrollment_count", "price"]
    ordering = ["-created_at"]

    def perform_create(self, serializer):
        if self.request.user.role != "Instructor":
            raise PermissionDenied("Only instructors can create courses")
        serializer.save(instructor=self.request.user)

    def perform_update(self, serializer):
        if serializer.instance.instructor != self.request.user:
            raise PermissionDenied("You can only update your own courses")
        serializer.save()
