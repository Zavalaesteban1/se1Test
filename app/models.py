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
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assignments')
    instructions_pdf = models.FileField(upload_to='assignment_pdfs/', null=True, blank=True)
    code_zip_file = models.FileField(upload_to='assignment_zips/', null=True, blank=True) 
    # Add these fields for better assignment management
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    completed = models.BooleanField(default=False, null=True, blank=True)
    class_name = models.CharField(max_length=100, default='Default Class')  # Add this line

    ### for when student submits 
    submitted_pdf = models.FileField(upload_to='submitted_pdfs/', null=True, blank=True)
    submitted_zip = models.FileField(upload_to='submitted_zips/', null=True, blank=True)
    submitted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.title} - Assigned to: {self.assigned_to.username}"

    class Meta:
        ordering = ['-created_at']
    