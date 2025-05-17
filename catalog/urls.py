from django.urls import path
from . import views
from .views import MyOpportunitiesView

app_name = 'catalog'

urlpatterns = [
    path('', views.index, name='index'),
    path('opportunity/<int:pk>/', views.OpportunityDetailView.as_view(), name='opportunity_detail'),
    path('my_opportunities/', MyOpportunitiesView.as_view(), name='my_opportunities'),
    path('organizer/<int:pk>/', views.OrganizerDetailView.as_view(), name='organizer_detail'),
    path('opportunities/', views.OpportunityListView.as_view(), name='opportunity_list'),
    path('my_events/', views.MyEventsView.as_view(), name='my_events'),

    # ─── Event URLs ──────────────────────────────────────────────────────────────
    path('events/',                views.EventListView.as_view(),    name='event_list'),
    path('events/new/',            views.EventCreateView.as_view(),  name='event_create'),
    path('events/<int:pk>/',       views.EventDetailView.as_view(),  name='event_detail'),
    path('events/<int:pk>/edit/',  views.EventUpdateView.as_view(),  name='event_edit'),
    path('events/<int:pk>/delete/',views.EventDeleteView.as_view(),  name='event_delete'),
    path('events/<int:event_id>/available-dates/', views.available_dates_view, name='available_dates'),
    path('available-date/<int:pk>/delete/', views.available_date_delete_view, name='available_date_delete'),
]
