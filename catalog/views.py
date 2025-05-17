from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    ListView, DetailView,
    CreateView, UpdateView, DeleteView
)
from django.urls import reverse_lazy

from .models import Opportunity, Signup, Organizer, Category, Event, AvailableDate
from .forms  import EventForm, AvailableDateForm

#Home Page

def index(request):
    """View function for home page of volunteering site."""

    num_opportunities = Opportunity.objects.count()
    num_signups = Signup.objects.count()

    # Signups with status 'c' (Confirmed)
    num_confirmed_signups = Signup.objects.filter(status='c').count()

    num_organizers = Organizer.objects.count()
    num_categories = Category.objects.count()

    context = {
        'num_opportunities': num_opportunities,
        'num_signups': num_signups,
        'num_confirmed_signups': num_confirmed_signups,
        'num_organizers': num_organizers,
        'num_categories': num_categories,
    }

    return render(request, 'index.html', context=context)

#Opportunities
# View that displays only the opportunities created by the logged-in user
class MyOpportunitiesView(LoginRequiredMixin, ListView):
    model = Opportunity
    template_name = 'catalog/my_opportunities.html'
    context_object_name = 'opportunities'

    def get_queryset(self):
        try:
            organizer = Organizer.objects.get(user=self.request.user)
            return Opportunity.objects.filter(organizer=organizer)
        except Organizer.DoesNotExist:
            return Opportunity.objects.none()

class OpportunityDetailView(DetailView):
    model = Opportunity
    template_name = 'catalog/opportunity_detail.html'
    context_object_name = 'opportunity'

class OrganizerDetailView(DetailView):
    model = Organizer
    template_name = 'catalog/organizer_detail.html'
    context_object_name = 'organizer'

class OpportunityListView(ListView):
    model = Opportunity
    template_name = 'catalog/opportunity_list.html'
    context_object_name = 'opportunities'

#Events CRUD

class EventListView(ListView):
    model = Event
    template_name = 'catalog/event_list.html'
    context_object_name = 'events'

class EventDetailView(DetailView):
    model = Event
    template_name = 'catalog/event_detail.html'
    context_object_name = 'event'

class EventCreateView(LoginRequiredMixin, CreateView):
    model = Event
    form_class = EventForm
    template_name = 'catalog/event_form.html'

    def form_valid(self, form):
        # Link the new Event to the logged-in user’s Organizer record
        form.instance.organizer = Organizer.objects.get(user=self.request.user)
        return super().form_valid(form)

class EventUpdateView(LoginRequiredMixin, UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'catalog/event_form.html'

    def get_queryset(self):
        # Only allow the organizer who created it to edit
        org = Organizer.objects.get(user=self.request.user)
        return Event.objects.filter(organizer=org)

class EventDeleteView(LoginRequiredMixin, DeleteView):
    model = Event
    template_name = 'catalog/event_confirm_delete.html'
    success_url = reverse_lazy('catalog:event_list')

    def get_queryset(self):
        org = Organizer.objects.get(user=self.request.user)
        return Event.objects.filter(organizer=org)




# View to display only the events created by the logged-in user
class MyEventsView(LoginRequiredMixin, ListView):
    model = Event
    template_name = 'catalog/my_events.html'
    context_object_name = 'events'

    def get_queryset(self):
        try:
            organizer = Organizer.objects.get(user=self.request.user)
            return Event.objects.filter(organizer=organizer)
        except Organizer.DoesNotExist:
            return Event.objects.none()
# Available Dates Management

def available_dates_view(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    form = AvailableDateForm()

    if request.method == 'POST':
        form = AvailableDateForm(request.POST)
        if form.is_valid():
            available_date = form.save(commit=False)
            available_date.event = event
            available_date.save()
            return redirect('catalog:available_dates', event_id=event.id)

    available_dates = event.available_dates.all().order_by('date')

    context = {
        'event': event,
        'form': form,
        'available_dates': available_dates
    }
    return render(request, 'catalog/available_dates.html', context)

def available_date_delete_view(request, pk):
    available_date = get_object_or_404(AvailableDate, pk=pk)
    event_id = available_date.event.id
    if request.method == 'POST':
        available_date.delete()
    return redirect('catalog:available_dates', event_id=event_id)


