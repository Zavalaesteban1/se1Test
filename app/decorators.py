from django.shortcuts import redirect
from functools import wraps

def student_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and hasattr(request.user, 'profile'):
            if request.user.profile.user_type == 'student':
                return view_func(request, *args, **kwargs)
        return redirect('home')
    return _wrapped_view



def admin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            user_type = request.session.get('user_type')
            if user_type == 'admin':
                return view_func(request, *args, **kwargs)
        return redirect('home')
    return _wrapped_view