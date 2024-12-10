def user_type(request):
    if request.user.is_authenticated and hasattr(request.user, 'profile'):
        return {'user_type': request.user.profile.user_type}
    return {'user_type': None}