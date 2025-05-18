from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Event, VolunteerRole, Registration


class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Role Info', {'fields': ('role',)}),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name')


admin.site.register(User, UserAdmin)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'location', 'category', 'type')
    search_fields = ('title', 'location')
    list_filter = ('category', 'type', 'date')


@admin.register(VolunteerRole)
class VolunteerRoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'time_commitment')
    search_fields = ('name',)


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'role', 'status', 'timestamp')
    list_filter = ('status', 'event', 'timestamp')
    search_fields = ('user__username', 'event__title', 'role__name')
    readonly_fields = ('timestamp',)
