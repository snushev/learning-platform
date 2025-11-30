from rest_framework import viewsets
from .models import Lesson
from .serializers import LessonSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.exceptions import PermissionDenied


class LessonViewset(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()

    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    ordering = ['order']
    filterset_fields = ['course']

    def perform_create(self, serializer):
        if course.instructor != self.request.user:
            raise PermissionDenied("You can only create lessons for your own courses")
        serializer.save()

    def perform_update(self, serializer):
        if serializer.instance.course.instructor != self.request.user:
            raise PermissionDenied("You can only update lessons for your own courses")
        serializer.save()

    def perform_create(self, serializer):
        course = serializer.validated_data.get('course')
        if course.instructor != self.request.user:
            raise PermissionDenied("You can only create lessons for your own courses")
        serializer.save()