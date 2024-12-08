from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profile
from .forms import SignUpForm
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
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
def newassignment(request):
    return render(request, 'admin/admin_forms.html')


@login_required(login_url='home')
def create_assignment(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        due_date = request.POST['dueDate']
        assigned_to = request.POST['assignedTo']
        instructions_pdf = request.FILES.get('instructionsPdf')
        code_zip_file = request.FILES.get('codeZipFile')


        ## testing
        print("Title:", title)
        print("Description:", description)
        print("Due Date:", due_date)
        print("Assigned To:", assigned_to)
        print("Instructions PDF:", instructions_pdf)
        print("Code ZIP File:", code_zip_file)

        # Save the uploaded PDF file
        pdf_url = None
        if instructions_pdf:
            pdf_file_name = default_storage.save(instructions_pdf.name, ContentFile(instructions_pdf.read()))
            pdf_url = default_storage.url(pdf_file_name)

        # Save the uploaded ZIP file
        zip_url = None
        if code_zip_file:
            zip_file_name = default_storage.save(code_zip_file.name, ContentFile(code_zip_file.read()))
            zip_url = default_storage.url(zip_file_name)

        # Create a dictionary to store the assignment data
        assignment_data = {
            'title': title,
            'description': description,
            'due_date': due_date,
            'assigned_to': assigned_to,
            'instructions_pdf': pdf_url,
            'code_zip_file': zip_url
        }

        # Save the assignment data to a JSON file
        assignments_dir = os.path.join(settings.BASE_DIR, 'assignments')
        os.makedirs(assignments_dir, exist_ok=True)
        assignment_file = os.path.join(assignments_dir, f'{title}.json')
        with open(assignment_file, 'w') as f:
            json.dump(assignment_data, f)

        return redirect('assignment_list')

    return render(request, 'admin/admin_forms.html')
## for testing purposes 
def assignment_list(request):
    assignments_dir = os.path.join(settings.BASE_DIR, 'assignments')
    os.makedirs(assignments_dir, exist_ok=True)  # Create the directory if it doesn't exist
    
    assignment_files = os.listdir(assignments_dir)

    assignments = []
    for file_name in assignment_files:
        file_path = os.path.join(assignments_dir, file_name)
        with open(file_path, 'r') as f:
            assignment_data = json.load(f)
            assignments.append(assignment_data)

    print("Assignments:", assignments)

    return render(request, 'admin/assignment_list.html', {'assignments': assignments})


@login_required(login_url='home')
def dashboard(request):
    context = {
        'active_assignments': [
            {
                'title': 'Assignment 1',
                'due_date': '2024-03-01',
                'students': [
                    {'name': 'Student 1'},
                    {'name': 'Student 2'},
                    {'name': 'Student 3'},
                ]
            },

            {
                'title': 'Assignment 2',
                'due_date': '2024-04-01',
                'students': [
                    {'name': 'Student 4'},
                    {'name': 'Student 4'},
                    {'name': 'Student 1'},
                ]
            },
            # Add more assignments as needed
        ],
      
        'pending_tasks': [
            {
                'title': 'Assignment 1',
                'notes': [
                    {'student': 'Student 1', 'message': 'Having trouble with question 3'},
                    {'student': 'Student 2', 'message': 'Need clarification on part 2'},
                ]
            },
            # Add more tasks as needed
        ],
        'completed_assignments': [
            {
                'title': 'Assignment 1',
                'completed_students': [
                    {'name': 'Student 1'},
                    {'name': 'Student 2'},
                ]
            },
            # Add more completed assignments as needed
            {
                'title': 'Assignment 2',
                'completed_students': [
                    {'name': 'Student 3'},
                    {'name': 'Student 1'},
                    {'name': 'Student 5'},
                ]
            }, 
        ],
        'satisfaction_feedback': [
            {
                'title': 'Assignment 1',
                'feedback': [
                    {'student': 'Student 1', 'message': 'Assignment was challenging but helpful'},
                    {'student': 'Student 2', 'message': 'Clear instructions, good learning experience'},
                ]
            },
            # Add more feedback as needed
        ]
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