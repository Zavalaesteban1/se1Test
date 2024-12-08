from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):

    ## inserted on the go
    USER_TYPES = (
        ('student', 'Student'),
        ('admin', 'Admin'),
    )

    ## inserted on the go

    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=100, default='Student')
    ## throwing off the database
    user_type = models.CharField(max_length=10, choices=USER_TYPES, default='admin')
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    
    def __str__(self):
        return self.user.username

    def get_full_name(self):
        return self.user.get_full_name() or self.user.username



class Assignment(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    due_date = models.DateField()
    assigned_to = models.CharField(max_length=100)
    instructions_pdf = models.FileField(upload_to='assignment_pdfs/', null=True, blank=True)
    code_zip_file = models.FileField(upload_to='assignment_zips/', null=True, blank=True) 
    