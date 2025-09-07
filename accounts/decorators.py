from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied
from functools import wraps

def owner_required(view_func):
    """
    Decorator for views that checks that the user is logged in and is an owner.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            from django.contrib.auth.views import redirect_to_login
            return redirect_to_login(request.get_full_path())
        
        if not hasattr(request.user, 'user_type') or request.user.user_type != 'owner':
            raise PermissionDenied("You must be an owner to access this page.")
        
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def renter_required(view_func):
    """
    Decorator for views that checks that the user is logged in and is a renter.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            from django.contrib.auth.views import redirect_to_login
            return redirect_to_login(request.get_full_path())
        
        if not hasattr(request.user, 'user_type') or request.user.user_type != 'renter':
            raise PermissionDenied("You must be a renter to access this page.")
        
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def user_type_required(user_type):
    """
    Generic decorator that checks for specific user type.
    Usage: @user_type_required('owner') or @user_type_required('renter')
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                from django.contrib.auth.views import redirect_to_login
                return redirect_to_login(request.get_full_path())
            
            if not hasattr(request.user, 'user_type') or request.user.user_type != user_type:
                raise PermissionDenied(f"You must be a {user_type} to access this page.")
            
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator