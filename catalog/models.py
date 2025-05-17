from django.db import models
from django.urls import reverse
import uuid
from django.contrib.auth.models import User

class Category(models.Model):
    """Model representing a category of volunteering (e.g., Environment, Health)."""
    name = models.CharField(max_length=200, help_text='Enter a category (e.g. Education, Environment)')

    def __str__(self):
        return self.name


class Organizer(models.Model):
    """Model representing the organizer of volunteering opportunities."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    organization = models.CharField(max_length=200, blank=True)
    email = models.EmailField()

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        return reverse('catalog:organizer_detail', args=[self.id])

    def __str__(self):
        return f'{self.first_name} {self.last_name} ({self.organization})'


class Opportunity(models.Model):
    """Model representing a volunteering opportunity."""
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=1000, help_text='Describe the opportunity.')
    organizer = models.ForeignKey(Organizer, on_delete=models.SET_NULL, null=True)
    categories = models.ManyToManyField(Category, help_text='Select categories for this opportunity')
    date = models.DateField()
    location = models.CharField(max_length=200)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('catalog:opportunity_detail', args=[self.id])


class Signup(models.Model):
    """Model representing a volunteer signing up for a specific opportunity."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique signup ID')
    opportunity = models.ForeignKey(Opportunity, on_delete=models.CASCADE)
    volunteer_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    signup_date = models.DateTimeField(auto_now_add=True)
    STATUS_CHOICES = [
        ('p', 'Pending'),
        ('c', 'Confirmed'),
        ('x', 'Cancelled'),
    ]
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='p')

    class Meta:
        ordering = ['signup_date']

    def __str__(self):
        return f'{self.volunteer_name} - {self.opportunity.title} ({self.get_status_display()})'


class Event(models.Model):
    """Model representing a local calendar event."""
    title       = models.CharField(max_length=200)
    description = models.TextField(blank=True, help_text='Optional description')
    organizer   = models.ForeignKey(Organizer, on_delete=models.SET_NULL, null=True)
    start_time  = models.DateTimeField()
    end_time    = models.DateTimeField()
    location    = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"{self.title} ({self.start_time:%Y-%m-%d %H:%M})"

    def get_absolute_url(self):
        return reverse('catalog:event_detail', args=[self.id])


