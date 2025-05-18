from django.urls import path
from . import views

urlpatterns = [
    # Home page
    path('', views.home, name='home'),

    # Authentication
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Event listing and detail views
    path('events/', views.event_list, name='event_list'),
    path('events/<int:event_id>/', views.event_detail, name='event_detail'),

    # Admin-only views (dashboard and event management)
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-dashboard/add-event/', views.add_event, name='add_event'),
    path('admin-dashboard/edit-event/<int:event_id>/', views.edit_event, name='edit_event'),
    path('admin-dashboard/delete-event/<int:event_id>/', views.delete_event, name='delete_event'),

    # Volunteer roles listing and management (admin)
    path('roles/', views.role_list, name='role_list'),

    # Logged-in user's registrations
    path('my-registrations/', views.my_registrations, name='my_registrations'),
]
