from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLES = (
        ("Instructor", "Instructor"),
        ("Student", "Student")
    )

    email = models.EmailField(max_length=100, unique=True)
    profile_picture = models.ImageField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    role = models.CharField(max_length=20, choices=ROLES)
