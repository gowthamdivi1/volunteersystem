from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings

from .models import Event, VolunteerRole, Registration
from .forms import UserRegisterForm, UserLoginForm, EventForm, VolunteerRoleForm, RegistrationForm


# Utility: Check if user is admin
def is_admin(user):
    return user.is_authenticated and getattr(user, 'role', '') == 'admin'


# Home page
def home(request):
    return render(request, 'catalog/home.html')


# Admin Dashboard
@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    total_events = Event.objects.count()
    total_roles = VolunteerRole.objects.count()
    total_registrations = Registration.objects.count()
    recent_registrations = Registration.objects.select_related('user', 'event', 'role').order_by('-timestamp')[:5]
    events = Event.objects.all().order_by('-date')

    context = {
        'total_events': total_events,
        'total_roles': total_roles,
        'total_registrations': total_registrations,
        'recent_registrations': recent_registrations,
        'events': events,
    }
    return render(request, 'catalog/admin_dashboard.html', context)


# Admin: Add Event
@login_required
@user_passes_test(is_admin)
def add_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Event created successfully.")
            return redirect('admin_dashboard')
    else:
        form = EventForm()
    return render(request, 'catalog/add_event.html', {'form': form})


# Admin: Edit Event
@login_required
@user_passes_test(is_admin)
def edit_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, "Event updated successfully.")
            return redirect('admin_dashboard')
    else:
        form = EventForm(instance=event)
    return render(request, 'catalog/edit_event.html', {'form': form, 'event': event})


# Admin: Delete Event
@login_required
@user_passes_test(is_admin)
def delete_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if request.method == 'POST':
        event.delete()
        messages.success(request, "Event deleted successfully.")
        return redirect('admin_dashboard')
    return render(request, 'catalog/delete_event.html', {'event': event})


# User registration
def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, 'catalog/register.html', {'form': form})


# User login
def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = UserLoginForm()
    return render(request, 'catalog/login.html', {'form': form})


# User logout
def logout_view(request):
    logout(request)
    return redirect('login')


# View all events
@login_required
def event_list(request):
    events = Event.objects.all().order_by('date')
    return render(request, 'catalog/event_list.html', {'events': events})


# Event details and registration
@login_required
def event_detail(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    already_registered = Registration.objects.filter(user=request.user, event=event).exists()

    if request.method == 'POST':
        if already_registered:
            messages.warning(request, "You have already registered for this event.")
            return redirect('event_list')

        form = RegistrationForm(request.POST)
        if form.is_valid():
            registration = form.save(commit=False)
            registration.user = request.user
            registration.event = event
            registration.save()

            # Email notification
            send_mail(
                subject='Registration Confirmed',
                message=(
                    f"Hi {request.user.first_name},\n\n"
                    f"You’ve successfully registered for '{event.title}' on {event.date} at {event.location}.\n\n"
                    "Thank you!"
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[request.user.email],
                fail_silently=False,
            )

            messages.success(request, "Successfully registered! Confirmation email sent.")
            return redirect('event_list')
    else:
        form = RegistrationForm()

    return render(request, 'catalog/event_detail.html', {
        'event': event,
        'form': form,
        'already_registered': already_registered
    })


# Admin: Manage volunteer roles
@login_required
@user_passes_test(is_admin)
def role_list(request):
    roles = VolunteerRole.objects.all()
    if request.method == 'POST':
        form = VolunteerRoleForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Role added successfully.")
            return redirect('role_list')
    else:
        form = VolunteerRoleForm()
    return render(request, 'catalog/role_list.html', {'roles': roles, 'form': form})


# Logged-in user's registration list
@login_required
def my_registrations(request):
    registrations = Registration.objects.select_related('event', 'role').filter(user=request.user)
    return render(request, 'catalog/my_registrations.html', {'registrations': registrations})
