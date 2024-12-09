from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('logout/',views.logout_user, name = 'logout'),
	path('register/', views.register_user, name = 'register'),


    # admin paths 
    path('management/dashboard/', views.dashboard, name='dashboard'),
    path('management/home/', views.home, name='admin_home'),
    path('management/forms/', views.create_assignment, name='newassignment'),
    path('management/profile/', views.profile_view, name='profile'),
    path('management/profile/edit/', views.edit_profile, name='edit_profile'),
    path('management/profile/change-password/', views.change_password, name='change_password'),
    path('management/assignments/', views.assignment_list, name='assignment_list'),


    ## students paths
    path('student/', views.student_home, name='student_home'),
    path('assignment/create/', views.create_assignment, name='create_assignment'),
    path('student/todo/', views.student_todo, name='student_todo'),
    path('student/submission/', views.student_submission, name='submissions'),
    path('student/profile/', views.student_profile, name='student_profile'),
    path('assignment/<int:assignment_id>/complete/', views.mark_assignment_complete, name='mark_assignment_complete'),
    path('assignment/<int:assignment_id>/', views.assignment_detail, name='assignment_detail'),

]