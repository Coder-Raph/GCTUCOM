# complaints/models.py
from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Complaint(models.Model):
    PENDING = 'Pending'
    SOLVED = 'Solved'

    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (SOLVED, 'Solved'),
    ]

    name = models.CharField(max_length=255)
    email = models.EmailField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name
