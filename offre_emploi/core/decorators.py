from django.http import HttpResponseForbidden
from django.contrib import messages
from django.shortcuts import redirect


# décorateur pour recruteur
def is_recruiter_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        # Vérifie si l'utilisateur a un objet 'Recruiter'
        if not hasattr(request.user, 'recruiter'):  # Vérifie si l'utilisateur est un recruteur
            return HttpResponseForbidden("Vous devez être recruteur pour accéder à cette page.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view

# décorateur pour candidat
def is_job_seeker_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not hasattr(request.user, 'role') or request.user.role != 'job_seeker':
            messages.error(request, 'Vous devez être candidat pour accéder à cette page.')
            return redirect('home')  # Redirige vers la page d'accueil ou une autre page
        return view_func(request, *args, **kwargs)
    return _wrapped_view
