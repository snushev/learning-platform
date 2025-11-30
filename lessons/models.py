from django.db import models
from courses.models import Course


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="course_lessons")
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    order = models.IntegerField()
    video_url = models.URLField(blank=True, null=True)
    video_file = models.FileField(blank=True, null=True)
    content_text = models.TextField(blank=True, null=True)
    duration_minutes = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

