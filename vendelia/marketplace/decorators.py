from django.http import HttpResponseForbidden

def bloquear_baneados(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_banned:
            return HttpResponseForbidden("Tu cuenta ha sido baneada. No puedes realizar esta acción.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view
