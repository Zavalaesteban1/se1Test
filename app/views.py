from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profile
from .forms import SignUpForm
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os

def home(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login Successful")
            return redirect('home')
        else:
            messages.error(request, "Login Error")  # Changed to error message
            return redirect('home')
    return render(request, 'admin/admin_home.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, "Logged out")
    return redirect('home')

def register_user(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "Sign In Successful")
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'authentication/register.html', {'form': form})

@login_required(login_url='home')
def forms(request):
    return render(request, 'admin/admin_forms.html')


@login_required(login_url='home')
def create_assignment(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        due_date = request.POST['dueDate']
        assigned_to = request.POST['assignedTo']
        instructions_pdf = request.FILES.get('instructionsPdf')

        # Save the uploaded PDF file
        if instructions_pdf:
            file_name = default_storage.save(instructions_pdf.name, ContentFile(instructions_pdf.read()))
            file_url = default_storage.url(file_name)
        # this will change when the data base works 

        ##########################################################

        # Create a dictionary to store the assignment data
        assignment_data = {
            'title': title,
            'description': description,
            'due_date': due_date,
            'assigned_to': assigned_to,
            'instructions_pdf': file_url
        }

        # Save the assignment data to a file (e.g., JSON or pickle)
        assignments_dir = os.path.join(settings.BASE_DIR, 'assignments')
        os.makedirs(assignments_dir, exist_ok=True)
        assignment_file = os.path.join(assignments_dir, f'{title}.json')
        with open(assignment_file, 'w') as f:
            json.dump(assignment_data, f)


        ##########################################################

        # Redirect or render a success page
        return redirect('assignment_list')

    # Render the form template for GET requests
    return render(request, 'admin/admin_forms.html')


@login_required(login_url='home')
def dashboard(request):
    context = {
        'active_assignments': 10,
        'pending_tasks': 7,
        'completed_assignments': 3,
        'satisfaction': '98%'
    }
    return render(request, 'admin/admin_dashboard.html', context)

@login_required(login_url='home')
def profile_view(request):
    # Get or create profile for the user
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST' and request.FILES.get('profile_picture'):
        try:
            # Delete old profile picture if it exists
            if profile.profile_picture:
                profile.profile_picture.delete()
            
            # Update with new profile picture
            profile.profile_picture = request.FILES['profile_picture']
            profile.save()
            
            messages.success(request, 'Profile picture updated successfully!')
            return redirect('profile')
        except Exception as e:
            messages.error(request, f'Error updating profile picture: {str(e)}')
    
    context = {
        'profile': {
            'name': request.user.get_full_name() or request.user.username,
            'role': 'Software Developer(Admin)',  # You might want to store this in the Profile model
            'email': request.user.email,
            'last_login': request.user.last_login,
            'profile_picture': profile.profile_picture if profile.profile_picture else None
        }
    }
    return render(request, 'admin/admin_profile.html', context)

@login_required(login_url='home')
def edit_profile(request):
    # Add edit profile logic here
    return render(request, 'edit_profile.html')

@login_required(login_url='home')
def change_password(request):
    # Add change password logic here
    return render(request, 'change_password.html')