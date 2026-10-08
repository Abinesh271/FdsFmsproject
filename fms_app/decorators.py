from functools import wraps
from django.contrib import messages
from django.shortcuts import redirect
from .models import UserProfile

def get_role(user):
    if user.is_superuser:
        return 'ADMIN'
    profile = getattr(user, 'userprofile', None)
    return profile.role if profile else 'FACULTY'


def role_required(*allowed_roles):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            role = get_role(request.user)
            if role not in allowed_roles:
                messages.error(request, 'You do not have permission to access this page.')
                return redirect('dashboard')
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator