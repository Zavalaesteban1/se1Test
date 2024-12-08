from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('newassignment/', views.newassignment, name='newassignment'),
    path('logout/',views.logout_user, name = 'logout'),
	path('register/', views.register_user, name = 'register'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/change-password/', views.change_password, name='change_password'),
    path('create_assignment/', views.create_assignment, name='create_assignment'),
    path('assignments/', views.assignment_list, name='assignment_list'),
    ## students paths
    path('student/', views.student_home, name='student_home'),
    path('student/todo/', views.student_todo, name='todo'),
    path('student/submission/', views.student_submission, name='submissions'),
    path('student/profile/', views.student_profile, name='student_profile'),

]