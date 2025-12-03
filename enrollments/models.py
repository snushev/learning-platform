from django.db import models
from users.models import User
from courses.models import Course
from lessons.models import Lesson


class Enrollment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="student_enrollments")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="course_enrollments")
    enrolled_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    progress_percentage = models.IntegerField(default=0)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student.username} enrolled in {self.course.title}"

    class Meta:
        unique_together = ['student', 'course']
    

class LessonProgress(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name='lesson_progress')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='lesson_progress_items')
    is_viewed = models.BooleanField(default=False)
    completion_percentage = models.IntegerField(default=0)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.enrollment.student.username} - {self.lesson.title}"

    class Meta:
        unique_together = ['enrollment', 'lesson']