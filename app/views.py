from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Profile

def home(request):
    return render(request, 'home.html')

def dashboard(request):
    return render(request, 'dashboard.html')

def forms(request):
    return render(request, 'forms.html')

def profile(request):
    return render(request, 'profile.html')


@login_required
def dashboard(request):
    context = {
        'active_assignments': 10,  # Replace with actual data
        'pending_tasks': 7,        # Replace with actual data
        'completed_assignments': 3, # Replace with actual data
        'satisfaction': '98%'      # Replace with actual data
    }
    return render(request, 'dashboard.html', context)

def dashboard(request):
    context = {
        'active_assignments': 10,  # You can replace these with actual data from your database
        'pending_tasks': 7,
        'completed_assignments': 3,
        'satisfaction': '98%'
    }
    return render(request, 'dashboard.html', context)

@login_required
def profile_view(request):
    profile = {
        'name': request.user.get_full_name() or request.user.username,
        'role': 'Supreme Admin',
        'email': request.user.email,
        'last_login': request.user.last_login,
    }
    return render(request, 'profile.html', {'profile': profile})

@login_required
def edit_profile(request):
    # Add edit profile logic here
    pass

@login_required
def change_password(request):
    # Add change password logic here
    pass

def profile_view(request):
    # Create a dictionary with fake profile data
    profile_data = {
        'name': 'Esteban Zavala',
        'role': 'Software Developer(Admin)',
        'email': 'zavala.esteban105690@gmail.com',
        'last_login': '2024-02-20 15:30:00'
    }
    
    # Pass the data to the template
    return render(request, 'profile.html', {'profile': profile_data})