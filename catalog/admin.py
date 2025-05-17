from django.contrib import admin
from .models import Opportunity, Organizer, Category, Signup, Event

# Volunteering-related models
admin.site.register(Opportunity)
admin.site.register(Organizer)
admin.site.register(Category)
admin.site.register(Signup)

# Event calendar
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_time', 'organizer')
    list_filter  = ('start_time', 'organizer')

