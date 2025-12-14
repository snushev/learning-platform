from rest_framework import viewsets
from .models import CourseRating
from .serializers import CourseRatingSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.exceptions import PermissionDenied, ValidationError


class CourseRatingViewset(viewsets.ModelViewSet):
    queryset = CourseRating.objects.all()
    serializer_class = CourseRatingSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filterset_fields = ["course", "rating"]

    def perform_update(self, serializer):
        if serializer.instance.student != self.request.user:  # ✅
            raise PermissionDenied("You can only update your own ratings")
        serializer.save()
        serializer.instance.course.update_average_rating()

    def perform_destroy(self, instance):
        if instance.student != self.request.user:  # ✅
            raise PermissionDenied("You can only delete your own ratings")
        course = instance.course
        instance.delete()
        course.update_average_rating()

    def perform_create(self, serializer):
        if self.request.user.role != "Student":
            raise PermissionDenied("Only students can rate courses")

        course = serializer.validated_data.get("course")
        from enrollments.models import Enrollment

        if not Enrollment.objects.filter(student=self.request.user, course=course).exists():
            raise PermissionDenied("You must be enrolled in the course to rate it")

        serializer.save(student=self.request.user)

        course.update_average_rating()
