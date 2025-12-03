from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .models import Enrollment, LessonProgress
from .serializers import EnrollmentSerializer, LessonProgressSerializer

class EnrollmentViewSet(viewsets.ModelViewSet):
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.role == "Student":
            return Enrollment.objects.filter(student=self.request.user)
        return Enrollment.objects.filter(course__instructor=self.request.user)
    
    def perform_create(self, serializer):
        if self.request.user.role != "Student":
            raise PermissionDenied("Only students can enroll in courses")
        
        course = serializer.validated_data.get('course')
        
        if not course.is_published:
            raise PermissionDenied("Cannot enroll in unpublished course")
        
        serializer.save(student=self.request.user)
        
        course.enrollment_count += 1
        course.save()
    
    def perform_destroy(self, instance):
        course = instance.course
        course.enrollment_count -= 1
        course.save()
        instance.delete()
    
    @action(detail=True, methods=['post'])
    def mark_lesson_viewed(self, request, pk=None):
        enrollment = self.get_object()
        lesson_id = request.data.get('lesson_id')
        
        if not lesson_id:
            return Response({"error": "lesson_id is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        lesson_progress, created = LessonProgress.objects.get_or_create(
            enrollment=enrollment,
            lesson_id=lesson_id,
            defaults={'is_viewed': True, 'completion_percentage': 100}
        )
        
        if not created:
            lesson_progress.is_viewed = True
            lesson_progress.completion_percentage = 100
            lesson_progress.save()
        
        total_lessons = enrollment.course.course_lessons.count()
        viewed_lessons = LessonProgress.objects.filter(
            enrollment=enrollment,
            is_viewed=True
        ).count()
        
        enrollment.progress_percentage = int((viewed_lessons / total_lessons) * 100) if total_lessons > 0 else 0
        
        if enrollment.progress_percentage == 100:
            enrollment.is_completed = True
            from django.utils import timezone
            enrollment.completed_at = timezone.now()
        
        enrollment.save()
        
        return Response({
            "message": "Lesson marked as viewed",
            "progress_percentage": enrollment.progress_percentage
        })