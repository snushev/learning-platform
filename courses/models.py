from django.db import models
from users.models import User


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Course(models.Model):
    LEVELS = (("beginner", "Beginner"), ("intermediate", "Intermediate"), ("advanced", "Advanced"))
    title = models.CharField(max_length=150)
    description = models.TextField(null=True, blank=True)
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cousres_owned")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="courses")
    level = models.CharField(max_length=20, choices=LEVELS)
    price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    image = models.ImageField(blank=True, null=True, upload_to="course_images/")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    enrollment_count = models.IntegerField(default=0, editable=False)

    def __str__(self):
        return self.title

    def get_enrollment_count(self):
        return self.enrollment_count
