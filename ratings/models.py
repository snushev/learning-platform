from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from users.models import User
from courses.models import Course


class CourseRating(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="student_ratings")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="course_ratings")
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    review_text = models.TextField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student.username} rated {self.course.title} - {self.rating}/5"

    class Meta:
        ordering = ["-created_at"]
        unique_together = ("student", "course")
