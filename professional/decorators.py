from django.http import HttpResponseForbidden

def professional_required(view_func):
    def wrapper(request, *args, **kwargs):

        if not request.user.is_authenticated:
            return HttpResponseForbidden("Login required")

        try:
            if request.user.profile.role != "PROFESSIONAL":
                return HttpResponseForbidden("Professionals only")
        except:
            return HttpResponseForbidden("No profile")

        return view_func(request, *args, **kwargs)

    return wrapper