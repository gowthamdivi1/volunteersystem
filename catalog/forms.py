from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, Event, VolunteerRole, Registration

# ✅ User registration form with role and email
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'Email'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'role']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),
            'role': forms.Select(attrs={'placeholder': 'Role'}),
        }


# ✅ Login form using built-in AuthenticationForm
class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))


# ✅ Event form used by admin/staff
class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'date', 'location', 'category', 'type']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Event Title'}),
            'date': forms.DateInput(attrs={'type': 'date'}),
            'location': forms.TextInput(attrs={'placeholder': 'Location'}),
            'category': forms.TextInput(attrs={'placeholder': 'Category'}),
            'type': forms.Select(),
        }


# ✅ Volunteer role creation/editing form
class VolunteerRoleForm(forms.ModelForm):
    class Meta:
        model = VolunteerRole
        fields = ['name', 'time_commitment']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Role Name'}),
            'time_commitment': forms.TextInput(attrs={'placeholder': 'e.g. 4 hours/week'}),
        }


# ✅ Registration form — only selects role
class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Registration
        fields = ['role']
        widgets = {
            'role': forms.Select()
        }
