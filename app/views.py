from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profile
from .forms import SignUpForm
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from .decorators import student_required
from .models import Assignment
from django.contrib.auth.models import User  # Add this import
from django.utils import timezone

import os

def home(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)


        if user is not None:
            login(request, user)
            messages.success(request, "Login Successful")


            # Redirect based on user type
            if hasattr(user, 'profile'):
                if user.profile.user_type == 'student':
                    return redirect('student_home')
                else:
                    return redirect('admin_home')
            return redirect('home')
        else:
            messages.error(request, "Login Error")  # Changed to error message
            return redirect('home')
    return render(request, 'management/admin_home.html', {})

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
            email = form.cleaned_data['email']


            # Determine user type based on email domain
            user_type = 'student' if email.endswith('.edu') else 'admin'

            # Create profile with determined user type
            Profile.objects.create(
                user=user,
                user_type=user_type,
                role='Student' if user_type == 'student' else 'Admin'
            )

            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "Registration Successful")
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'authentication/register.html', {'form': form})

@login_required(login_url='home')
def admin_home(request):
    # Simply render the admin home template with the user context
    context = {
        'user': request.user,
    }
    return render(request, 'management/admin_home.html', context)

@login_required(login_url='home')
def newassignment(request):
    return render(request, 'management/admin_forms.html')


@login_required(login_url='home')
def create_assignment(request):
    students = Profile.objects.filter(
        user_type='student',
        user__email__endswith='@utrgv.edu'
    ).select_related('user')

    if request.method == 'POST':
        try:
            # Debug prints
            print("Form data received:")
            print(f"Title: {request.POST.get('title')}")
            print(f"Assigned To Email: {request.POST.get('assignedTo')}")
            print(f"Due Date:: {request.POST.get('dueDate')}")
            print(f"description: {request.POST.get('description')}")
            
            title = request.POST['title']
            description = request.POST['description']
            due_date = request.POST['dueDate']
            class_name = request.POST['className']
            instructions_pdf = request.FILES.get('instructionsPdf')
            code_zip_file = request.FILES.get('codeZipFile')

            print(f"Pdf: {request.POST.get('instructionsPdf')}")
            print(f"zip: {request.POST.get('codeZipFile')}")

            # Get the user instance
            assigned_to = User.objects.get(email=request.POST['assignedTo'])
            
            # Debug print
            print(f"Found user: {assigned_to.email}")

            # Create the assignment
            assignment = Assignment.objects.create(
                title=title,
                description=description,
                due_date=due_date,
                class_name=class_name,
                assigned_to=assigned_to,
                instructions_pdf=instructions_pdf,
                code_zip_file=code_zip_file,
                created_at=timezone.now(),
                completed=False
            )
            
            print(f"Assignment created: {assignment.title}")

            messages.success(request, f"Assignment '{title}' created successfully and assigned to {assigned_to.email}")
            return redirect('admin_home')

        except User.DoesNotExist:
            messages.error(request, "Selected student does not exist.")
            print("User does not exist error")
        except Exception as e:
            messages.error(request, f"Error creating assignment: {str(e)}")
            print(f"Error: {str(e)}")
        
        return redirect('create_assignment')

    context = {
        'students': students,
    }
    return render(request, 'management/admin_forms.html', context)
 
## for testing purposes 
@login_required(login_url='home')
def assignment_list(request):
    assignments = Assignment.objects.all()
    return render(request, 'management/assignment_list.html', {'assignments': assignments})



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
    return render(request, 'management/admin_dashboard.html', context)

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
    return render(request, 'management/admin_profile.html', context)

@login_required(login_url='home')

def edit_profile(request):
    # Add edit profile logic here
    return render(request, 'edit_profile.html')

@login_required(login_url='home')
def change_password(request):
    # Add change password logic here
    return render(request, 'change_password.html')



@login_required
@student_required
def student_home(request):
    context = {
        'user_type': request.user.profile.user_type
    }
    return render(request, 'student/student_home.html', context)

@login_required
@student_required
def student_todo(request):
    print(f"Current user: {request.user.email}")  # Debug print
    
    # Get active (not completed) assignments for the current student
    active_assignments = Assignment.objects.filter(
        assigned_to=request.user,
        completed=False
    ).order_by('due_date')
    
    # Debug print
    print(f"Found assignments: {active_assignments.count()}")
    for assignment in active_assignments:
        print(f"Assignment: {assignment.title} - {assignment.class_name}")

    # Get completed assignments count
    completed_assignments_count = Assignment.objects.filter(
        assigned_to=request.user,
        completed=True
    ).count()

    context = {
        'active_assignments': active_assignments,
        'pending_tasks': active_assignments.count(),
        'completed_assignments': completed_assignments_count,
        'satisfaction': '100%'
    }
    
    return render(request, 'student/student_todo.html', context)


@login_required
@student_required
def student_submission(request):
    context = {
        'user_type': request.user.profile.user_type
    }
    return render(request, 'student/student_submission.html', context)

@login_required
@student_required
def student_profile(request):
    # Get the profile for the logged-in user
    profile = Profile.objects.get(user=request.user)

    if request.method == 'POST' and request.FILES.get('profile_picture'):
        try:
            # Handle profile picture upload
            if profile.profile_picture:
                profile.profile_picture.delete()
            profile.profile_picture = request.FILES['profile_picture']
            profile.save()
            messages.success(request, 'Profile picture updated successfully!')
            return redirect('student_profile')
        except Exception as e:
            messages.error(request, f'Error updating profile picture: {str(e)}')
    

    context = {
        'user_type': 'student',
        'profile': {
            'name': request.user.get_full_name() or request.user.username,
            'role': profile.role,  # This will show 'Student' based on your Profile model
            'email': request.user.email,
            'last_login': request.user.last_login,
            'profile_picture': profile.profile_picture if profile.profile_picture else None
        }
    }

    
    return render(request, 'student/student_profile.html', context)


# For marking assignments as complete (you might want to add this)
@login_required
@student_required
def mark_assignment_complete(request, assignment_id):
    try:
        assignment = Assignment.objects.get(id=assignment_id, assigned_to=request.user)
        assignment.completed = True
        assignment.save()
        messages.success(request, "Assignment marked as complete!")
    except Assignment.DoesNotExist:
        messages.error(request, "Assignment not found.")
    
    return redirect('student_todo')

# For viewing assignment details (optional)
@login_required
@student_required
def assignment_detail(request, assignment_id):
    try:
        assignment = Assignment.objects.get(id=assignment_id, assigned_to=request.user)
        return render(request, 'student/assignment_detail.html', {'assignment': assignment})
    except Assignment.DoesNotExist:
        messages.error(request, "Assignment not found.")
        return redirect('student_todo')