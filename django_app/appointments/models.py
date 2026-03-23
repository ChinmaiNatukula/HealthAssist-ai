from django.db import models
from django.contrib.auth.models import User


class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments')
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    problem = models.TextField()
    preferred_date = models.DateField()
    preferred_time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.preferred_date} ({self.status})"
