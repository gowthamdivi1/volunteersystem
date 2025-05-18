from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('volunteer', 'Volunteer'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='volunteer')

    def __str__(self):
        return self.username


class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(default='No description provided.')  # Clear field name
    date = models.DateTimeField()
    location = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    type = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.title} on {self.date.strftime('%Y-%m-%d')}"


class VolunteerRole(models.Model):
    name = models.CharField(max_length=100)
    time_commitment = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Registration(models.Model):
    STATUS_CHOICES = (
        ('confirmed', 'Confirmed'),
        ('pending', 'Pending'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    role = models.ForeignKey(VolunteerRole, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.event.title} ({self.status})'
