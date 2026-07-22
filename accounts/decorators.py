from functools import wraps
from django.contrib import messages
from django.shortcuts import redirect


def role_required(*roles):
    """Restrict a view to users whose .role is in `roles` (superusers always allowed)."""
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect("accounts:login")
            if request.user.is_superuser or request.user.role in roles:
                return view_func(request, *args, **kwargs)
            messages.error(request, "You don't have permission to access that page.")
            return redirect("dashboard:redirect")
        return _wrapped
    return decorator
